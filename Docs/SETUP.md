# Central Query Brain - Setup Guide

This guide will walk you through setting up CQB on your system.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **RAM**: 16GB system RAM
- **Storage**: 20GB free space for models

### Recommended Requirements
- **Python**: 3.10+
- **GPU**: NVIDIA A100, RTX 4090, or RTX 3090 with 16GB+ VRAM
- **RAM**: 32GB+ system RAM
- **Storage**: 50GB+ SSD storage

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/central-query-brain.git
cd central-query-brain
```

### 2. Set Up Python Environment

Using conda (recommended):
```bash
conda create -n cqb python=3.10
conda activate cqb
```

Using venv:
```bash
python -m venv cqb_env
source cqb_env/bin/activate  # Linux/Mac
# or
cqb_env\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For development setup:
```bash
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### 4. Configure Models

Copy the configuration template:
```bash
cp config.yaml.template config.yaml
```

Edit `config.yaml` to match your hardware:

**For 8-12GB VRAM setups:**
```yaml
conservative_model:
  memory_fraction: 0.3
  max_model_len: 2048

innovative_model:
  memory_fraction: 0.4
  max_model_len: 2048
```

**For 16-24GB VRAM setups:**
```yaml
conservative_model:
  memory_fraction: 0.4
  max_model_len: 4096

innovative_model:
  memory_fraction: 0.5
  max_model_len: 4096
```

**For 40GB+ VRAM setups:**
```yaml
conservative_model:
  memory_fraction: 0.6
  max_model_len: 8192

innovative_model:
  memory_fraction: 0.7
  max_model_len: 8192
```

### 5. Test Installation

Run the basic test:
```bash
python -c "
from cqb_framework import initialize_cqb
cqb = initialize_cqb()
if cqb:
    print('✅ CQB initialized successfully!')
else:
    print('❌ CQB initialization failed')
"
```

### 6. Run Example

Test with a simple example:
```bash
python examples/techflow_crisis.py
```

## Model Selection Guide

### Conservative Models (Analytical Reasoning)
- **Recommended**: `hugging-quants/gemma-2-9b-it-AWQ-INT4`
- **Alternative**: `TheBloke/Llama-2-13B-Chat-AWQ`
- **Budget**: `microsoft/DialoGPT-medium`

### Innovative Models (Creative Reasoning)
- **Recommended**: `Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4`
- **Alternative**: `TheBloke/Mixtral-8x7B-Instruct-v0.1-AWQ`
- **Budget**: `microsoft/DialoGPT-large`

### Quantization Options
- **AWQ**: Best for inference speed, requires AWQ-compatible models
- **GPTQ**: Good balance of speed and quality
- **None**: Full precision, requires more VRAM

## Troubleshooting

### Common Issues

#### "CUDA out of memory"
- Reduce `memory_fraction` in config.yaml
- Lower `max_model_len`
- Use smaller models
- Enable `enforce_eager: true`

#### "Model not found"
- Verify model path in config.yaml
- Check internet connection for model download
- Ensure you have access to the model repository

#### "Import Error"
- Verify all dependencies installed: `pip list`
- Check Python version: `python --version`
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

#### "vLLM initialization failed"
- Try `enforce_eager: true` in config
- Check CUDA installation: `nvidia-smi`
- Verify PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`

### Performance Optimization

#### For Better Speed
- Use AWQ quantization
- Enable chunked prefill
- Increase `max_num_seqs`
- Use tensor parallelism for large models

#### For Better Quality
- Use larger models
- Disable quantization if VRAM allows
- Increase `max_model_len`
- Use higher `top_p` values

#### For Memory Efficiency
- Enable quantization
- Lower `memory_fraction`
- Reduce `max_model_len`
- Use gradient checkpointing

## Advanced Configuration

### Multi-GPU Setup

For multiple GPUs, modify config.yaml:
```yaml
conservative_model:
  tensor_parallel_size: 2  # Use 2 GPUs
  
innovative_model:
  tensor_parallel_size: 2  # Use 2 GPUs
```

### Custom Models

To use your own models:
```yaml
conservative_model:
  model_path: '/path/to/your/model'
  # or
  model_path: 'your-username/your-model-name'
```

### Environment Variables

Set these for better performance:
```bash
export CUDA_VISIBLE_DEVICES=0,1  # Specify GPU devices
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export TOKENIZERS_PARALLELISM=false
```

## Validation

After setup, validate your installation:

```bash
# Test model loading
python -c "
from cqb_framework import initialize_cqb
cqb = initialize_cqb()
print('Available models:', cqb.model_manager.get_available_models())
print('System status:', cqb.model_manager.get_loaded_models())
"

# Test agent generation
python -c "
from cqb_framework import initialize_cqb
from collaboration_module import AgentCollaborationModule

cqb = initialize_cqb()
collab = AgentCollaborationModule(cqb)
session_id = collab.collaborate_on_query('Test query', max_agents=2, collaboration_rounds=1)
print('✅ Full pipeline test successful!')
"
```

## Next Steps

1. **Run Examples**: Try all examples in the `examples/` directory
2. **Customize Configuration**: Tune settings for your hardware
3. **Develop Custom Scenarios**: Create your own collaboration scenarios
4. **Monitor Performance**: Use the JSON outputs to analyze system performance

## Getting Help

- **Issues**: Check the GitHub Issues page
- **Discussions**: Join the GitHub Discussions
- **Documentation**: See `docs/` directory for detailed guides
- **Examples**: Study the `examples/` directory for usage patterns
