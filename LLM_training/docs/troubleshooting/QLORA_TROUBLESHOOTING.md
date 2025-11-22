# QLoRA Training Troubleshooting Guide

## Quick Diagnosis

### Symptom 1: Training Freezes at 0%

```
Training:   0%|          | 0/1207 [00:00<?, ?it/s]
```

**Cause**: Incorrect loss computation (manual log_softmax)

**Fix**: Applied in Cell 19 - use `nn.losses.cross_entropy()`

**Verification**: Training should advance within 10-20 seconds

---

### Symptom 2: NaN Loss Values

```
  Step 20/1207 - Loss: nan
```

**Causes**:
1. Loss computation creating NaN gradients
2. Learning rate too high
3. Gradient explosion

**Fixes**:
```python
# 1. Already fixed in Cell 19 (use cross_entropy)

# 2. Reduce learning rate
training_config['learning_rate'] = 5e-5  # Down from 2e-4

# 3. Add gradient clipping
def clip_grads(grads, max_norm=1.0):
    total_norm = 0
    for key in grads:
        total_norm += mx.sum(grads[key] ** 2)
    total_norm = mx.sqrt(total_norm)

    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        for key in grads:
            grads[key] = grads[key] * clip_coef
    return grads

# Apply in train_epoch before optimizer.update:
accumulated_grads = clip_grads(accumulated_grads, max_norm=1.0)
optimizer.update(model, accumulated_grads)
```

---

### Symptom 3: Memory Keeps Increasing

```
[Memory] Step 20: 3000MB available
[Memory] Step 40: 2500MB available
[Memory] Step 60: 2000MB available
[Memory] Step 80: 1500MB available
[Memory] Step 100: 1000MB available
⚠ WARNING: Low memory (1000MB)
```

**Causes**:
1. Lazy evaluation buildup (missing mx.eval())
2. Memory cleanup frequency too low
3. Batch size too large

**Fixes**:
```python
# 1. Already fixed in Cell 19 (mx.eval(loss_val))

# 2. Increase cleanup frequency
training_config['memory_cleanup_steps'] = 3  # Down from 5

# 3. Reduce batch size
training_config['batch_size'] = 1  # Down from 2
training_config['gradient_accumulation'] = 4  # Up from 2
```

---

### Symptom 4: Training Very Slow

```
Training:   1%|▏| 12/1207 [05:00<8:15:00, 24.87s/it]
```

**Causes**:
1. CPU mode instead of GPU
2. Sequence length too long
3. Model not quantized

**Fixes**:
```python
# 1. Verify GPU is enabled
import mlx.core as mx
print(f"Device: {mx.default_device()}")  # Should be "gpu"

# Force GPU if needed
mx.set_default_device(mx.gpu)

# 2. Reduce sequence length
training_config['max_seq_length'] = 256  # Down from 512

# 3. Verify quantization
# Check during model loading:
# model, tokenizer = load(MODEL_NAME, quantization="int4")
```

---

### Symptom 5: Loss Not Decreasing

```
  Step 100/1207 - Loss: 8.4523
  Step 200/1207 - Loss: 8.4891
  Step 300/1207 - Loss: 8.4234
```

**Causes**:
1. Learning rate too low
2. Gradients not being applied
3. Data quality issues

**Fixes**:
```python
# 1. Increase learning rate
training_config['learning_rate'] = 3e-4  # Up from 2e-4

# 2. Verify gradients are applied (already fixed in Cell 19)

# 3. Check data quality
for i in range(5):
    item = train_dataset[i]
    print(f"Example {i}: {item['input_ids'][:20]}")
    # Should show varied, non-zero token IDs
```

---

### Symptom 6: Validation Loss Much Higher Than Training Loss

```
  Epoch 1 - Avg Loss: 4.2341
  Val Loss: 12.5432
```

**Causes**:
1. Overfitting
2. Data leakage
3. Different loss computation in validation

**Fixes**:
```python
# 1. Add dropout
lora_config['lora_dropout'] = 0.1  # Up from 0.05

# 2. Verify train/val split
print(f"Train examples: {len(train_data)}")
print(f"Val examples: {len(val_data)}")
# Should be 90/10 split

# 3. Already fixed in Cell 19 (same loss computation)
```

---

### Symptom 7: CUDA/Metal Errors

```
[ERROR] Metal device error: command buffer execution failed
```

**Causes**:
1. Out of memory
2. Invalid tensor operations
3. Driver issues

**Fixes**:
```python
# 1. Reduce memory usage
training_config['batch_size'] = 1
training_config['max_seq_length'] = 256
training_config['memory_cleanup_steps'] = 3

# 2. Add error recovery
try:
    loss_val, grads = mx.value_and_grad(loss_fn)(model)
except Exception as e:
    print(f"[ERROR] {e}")
    memory_monitor.cleanup()
    continue

# 3. Update drivers (outside notebook)
# brew upgrade mlx
```

---

## Emergency Procedures

### If Training Crashes Mid-Epoch

```python
# 1. Check last checkpoint
import json
with open('checkpoints_qlora/training_state.json', 'r') as f:
    state = json.load(f)
print(f"Last epoch: {state['epoch']}")
print(f"Last step: {state['step']}")

# 2. Resume from checkpoint
tracker = TrainingTracker(CHECKPOINTS_DIR)
# Will automatically load state

# 3. Restart training (skips completed epochs)
for epoch in range(tracker.state['epoch'], training_config['num_epochs']):
    # Training continues from saved state
```

### If Notebook Kernel Crashes

```bash
# 1. Check system resources
top -l 1 | head -n 10

# 2. Clear memory
# Restart Jupyter kernel

# 3. Resume training
# Run cells 1-18 (setup)
# Run cell 19 (functions)
# Run cell 20 (training)
# Automatically resumes from last checkpoint
```

### If Loss Explodes

```python
# 1. Stop training immediately (KeyboardInterrupt)

# 2. Load last good checkpoint
last_good = 'checkpoints_qlora/checkpoint_epoch0_step200'
model, tokenizer = load(
    "mistralai/Mistral-7B-v0.1",
    adapter_path=last_good
)

# 3. Reduce learning rate
training_config['learning_rate'] = 1e-5  # Much lower

# 4. Add gradient clipping (see Symptom 2)

# 5. Resume training
```

---

## Verification Checklist

After applying the fix, verify:

### Immediate (First 60 seconds)
- [ ] Cell 19 runs without errors
- [ ] Cell 20 starts training loop
- [ ] Progress bar appears
- [ ] Step 0 completes (10-20 seconds)
- [ ] Progress bar advances to 1/1207

### Short-term (First 5 minutes)
- [ ] Step 20: Loss prints (~8-12 initially)
- [ ] Memory logging shows stable usage
- [ ] No error messages
- [ ] Progress bar advancing smoothly
- [ ] Each step takes 5-10 seconds

### Medium-term (First 30 minutes)
- [ ] Step 100: Validation runs
- [ ] Step 200: Checkpoint saves
- [ ] Loss decreasing (down to ~6-8)
- [ ] Memory stable (4-6GB)
- [ ] No crashes or freezes

### Long-term (Full epoch)
- [ ] Epoch completes (~2-3 hours)
- [ ] Average epoch loss printed
- [ ] Validation loss printed
- [ ] Best model saved
- [ ] Ready for epoch 2

---

## Performance Targets

### Expected Metrics (M1 Pro/Max)

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Step time | 5-10s | >15s | >30s |
| Memory usage | 4-6GB | >8GB | >10GB |
| Initial loss | 8-12 | >15 | >20 |
| Loss after 100 steps | 6-8 | >10 | Same as initial |
| Loss after 500 steps | 4-6 | >8 | Increasing |
| Tokens/second | 300-500 | <200 | <100 |

### If Below Targets:

**Step time too slow (>15s)**:
- Reduce `max_seq_length` to 256
- Check GPU is enabled
- Close other applications

**Memory usage too high (>8GB)**:
- Reduce `batch_size` to 1
- Increase `memory_cleanup_steps` to 3
- Reduce `max_seq_length` to 256

**Loss not decreasing**:
- Increase `learning_rate` to 3e-4
- Check data quality
- Verify gradients are applied

---

## Common Mistakes

### 1. Not Running Cell 19 After Edit

**Problem**: Old broken functions still loaded

**Solution**: Always run Cell 19 before Cell 20

### 2. Reusing Old Checkpoints

**Problem**: Broken state from previous run

**Solution**: Clear checkpoints before restarting
```bash
rm -rf checkpoints_qlora/*
```

### 3. Not Monitoring Memory

**Problem**: Crashes without warning

**Solution**: Watch memory logs
```
[Memory] Step 20: 5000MB available
```

### 4. Stopping Training Too Early

**Problem**: Loss hasn't converged yet

**Solution**: Let at least 1 full epoch complete (~2-3 hours)

### 5. Not Validating Fix Applied

**Problem**: Still using broken version

**Solution**: Check Cell 19 contains:
```python
loss = nn.losses.cross_entropy(
    logits_flat,
    labels_flat,
    reduction="mean"
)
```

---

## Getting Help

### What to Include in Bug Report:

1. **Symptom**: What's happening?
   ```
   Training freezes at 0%
   ```

2. **Last output**: Copy last 20 lines
   ```
   [Memory] Epoch 1 start: 3471MB available
   Training:   0%|          | 0/1207 [00:00<?, ?it/s]
   ```

3. **System info**:
   ```python
   import platform
   print(f"System: {platform.system()}")
   print(f"Machine: {platform.machine()}")
   print(f"MLX device: {mx.default_device()}")
   ```

4. **Config**:
   ```python
   print(training_config)
   print(lora_config)
   ```

5. **Memory**:
   ```python
   memory_monitor.log_memory("Current")
   ```

---

## Success Indicators

You'll know the fix worked when:

1. Training advances past 0% immediately
2. Loss values print every 20 steps
3. Loss decreases over time
4. Memory usage stays stable
5. Validation runs at step 100
6. Checkpoints save at step 200
7. Epoch completes successfully
8. No error messages appear

Expected timeline:
- **0-20 seconds**: First step completes
- **5 minutes**: 60 steps done
- **15 minutes**: First validation
- **30 minutes**: First checkpoint
- **2-3 hours**: First epoch complete

If you hit these milestones, the fix is working correctly!
