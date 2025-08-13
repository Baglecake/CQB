
# =============================================================================
# vLLM LangExtract Adapter - Bridge between CQB and LangExtract
# =============================================================================

import time
from typing import Iterator, Sequence, Any, Dict
from collections.abc import Mapping
from dataclasses import dataclass

# LangExtract imports (adapted from the provided files)
from cqb.langextract.inference import BaseLanguageModel, ScoredOutput, InferenceOutputError

# =============================================================================
# vLLM Language Model Adapter
# =============================================================================

@dataclass
class VLLMLanguageModel(BaseLanguageModel):
    """LangExtract-compatible language model adapter for CQB's vLLM backend.
    
    This adapter allows LangExtract to use CQB's existing vLLM models instead of
    requiring separate Ollama/Gemini API calls.
    """
    
    def __init__(self, cqb_model_manager, model_id: str = "conservative_model", 
                 temperature: float = 0.3, max_workers: int = 1, **kwargs):
        """Initialize the vLLM adapter.
        
        Args:
            cqb_model_manager: CQB's model manager instance
            model_id: Which CQB model to use ("conservative_model" or "innovative_model")
            temperature: Sampling temperature for extraction
            max_workers: Number of parallel workers (kept at 1 for GPU memory efficiency)
            **kwargs: Additional parameters (for compatibility)
        """
        self.model_manager = cqb_model_manager
        self.model_id = model_id
        self.temperature = temperature
        self.max_workers = max_workers
        self.extra_kwargs = kwargs
        
        # Initialize base class
        super().__init__()
        
        print(f"✅ VLLMLanguageModel initialized with {model_id}")
    
    def infer(self, batch_prompts: Sequence[str], **kwargs) -> Iterator[Sequence[ScoredOutput]]:
        """Run inference on batch of prompts using CQB's vLLM models.
        
        Args:
            batch_prompts: List of prompts to process
            **kwargs: Additional generation parameters
            
        Yields:
            Sequences of ScoredOutput objects
            
        Raises:
            InferenceOutputError: If inference fails
        """
        
        # Extract generation parameters
        temperature = kwargs.get('temperature', self.temperature)
        max_output_tokens = kwargs.get('max_output_tokens', 1024)
        
        # Process each prompt (sequential for GPU memory efficiency)
        for i, prompt in enumerate(batch_prompts):
            try:
                # Use CQB's model manager for generation
                response = self.model_manager.generate_text(
                    model_id=self.model_id,
                    prompt=prompt,
                    temperature=temperature
                )
                
                # Wrap in LangExtract's expected format
                scored_output = ScoredOutput(score=1.0, output=response)
                yield [scored_output]
                
                # Optional: Add small delay between requests for stability
                if i < len(batch_prompts) - 1:
                    time.sleep(0.1)
                    
            except Exception as e:
                error_msg = f"vLLM inference failed for prompt {i+1}/{len(batch_prompts)}: {str(e)}"
                print(f"❌ {error_msg}")
                raise InferenceOutputError(error_msg) from e
    
    def generate_single(self, prompt: str, **kwargs) -> str:
        """Convenience method for single prompt generation.
        
        Args:
            prompt: Single prompt to process
            **kwargs: Generation parameters
            
        Returns:
            Generated text response
        """
        try:
            results = list(self.infer([prompt], **kwargs))
            return results[0][0].output
        except Exception as e:
            raise InferenceOutputError(f"Single generation failed: {str(e)}") from e
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the underlying model.
        
        Returns:
            Dictionary with model information
        """
        return {
            'backend': 'vLLM',
            'model_id': self.model_id,
            'temperature': self.temperature,
            'max_workers': self.max_workers,
            'adapter_version': '1.0.0'
        }

# =============================================================================
# Testing and Validation
# =============================================================================

def test_vllm_adapter(cqb_model_manager):
    """Test the vLLM adapter with a simple prompt.
    
    Args:
        cqb_model_manager: Initialized CQB model manager
        
    Returns:
        bool: True if test passes
    """
    print("🧪 Testing vLLM LangExtract Adapter...")
    
    try:
        # Initialize adapter
        adapter = VLLMLanguageModel(
            cqb_model_manager=cqb_model_manager,
            model_id="conservative_model",
            temperature=0.3
        )
        
        # Test prompt
        test_prompt = """Extract key information from this text:
        
Budget: $2.1M annual, 25 representatives handling 5,000+ monthly interactions.
Current satisfaction: 3.2/5.0, response time: 48 hours.

Provide a structured summary of the metrics found."""
        
        # Test single inference
        response = adapter.generate_single(test_prompt)
        
        print(f"✅ Test Response ({len(response)} chars):")
        print(f"   {response[:100]}...")
        
        # Test batch inference
        batch_prompts = [
            "What is artificial intelligence?",
            "Explain machine learning briefly."
        ]
        
        batch_results = list(adapter.infer(batch_prompts))
        print(f"✅ Batch test: {len(batch_results)} responses generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Adapter test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 vLLM LangExtract Adapter")
    print("=" * 50)
    print("This adapter bridges CQB's vLLM models with LangExtract's extraction engine.")
    print("\nUsage:")
    print("  adapter = VLLMLanguageModel(cqb_model_manager)")
    print("  response = adapter.generate_single(prompt)")
    print("  batch_results = list(adapter.infer(batch_prompts))")
