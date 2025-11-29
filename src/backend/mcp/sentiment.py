from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import torch
import warnings

# STRICT REQUIREMENT: Use ProsusAI/finbert
MODEL_NAME = "ProsusAI/finbert"

nlp = None

# Suppress warnings and try to load model
warnings.filterwarnings('ignore')
try:
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
    # Pipeline handles the complexity of logits -> probabilities
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
except Exception as e:
    # Fail gracefully - sentiment analysis is optional
    error_msg = str(e)
    if "torch" in error_msg.lower() or "weight" in error_msg.lower():
        # Don't print torch version errors, they're expected
        pass
    else:
        warnings.warn(f"⚠️ FinBERT sentiment analysis unavailable: {error_msg}")

def analyze_sentiment(text):
    """
    Analyzes text using ProsusAI FinBERT.
    Returns: Report string.
    """
    if nlp is None:
        return "Model Error: FinBERT failed to initialize. Check your PyTorch version/Internet connection.", "Error"

    if not text or len(text.strip()) < 20:
        return "Text provided is too short for meaningful financial analysis.", "Skipped"

    # Chunking: FinBERT has a 512 token limit.
    # We split by sentences to preserve context.
    sentences = text.split('.')
    chunks = []
    current_chunk = ""

    for sent in sentences:
        if len(current_chunk) + len(sent) < 500:
            current_chunk += sent + "."
        else:
            chunks.append(current_chunk)
            current_chunk = sent + "."
    if current_chunk: chunks.append(current_chunk)

    results = []
    try:
        # Process first 20 chunks to balance speed/coverage
        for chunk in chunks[:20]: 
            if len(chunk.strip()) > 5:
                # Truncation ensures we don't crash on weird long strings
                res = nlp(chunk, truncation=True, max_length=512)[0]
                results.append(res)
    except Exception as e:
        return f"Analysis Error: {str(e)}", "Error"

    if not results:
        return "Could not extract valid text segments.", "Error"

    # ProsusAI Output labels: 'positive', 'negative', 'neutral'
    counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    scores = {'positive': 1, 'neutral': 0, 'negative': -1}
    
    total_score = 0
    
    for r in results:
        label = r['label'].lower()
        if label in counts:
            counts[label] += 1
            total_score += scores[label]

    # Calculate weighted sentiment score
    avg_score = total_score / len(results)
    dominant_sentiment = max(counts, key=counts.get)

    report = (
        f"### 🤖 ProsusAI FinBERT Analysis\n"
        f"**Dominant Tone:** {dominant_sentiment.upper()}\n"
        f"**Financial Sentiment Score:** {avg_score:.2f} (Range: -1.0 to +1.0)\n\n"
        f"**Detailed Breakdown:**\n"
        f"📈 Positive Statements: {counts['positive']}\n"
        f"📉 Negative Statements: {counts['negative']}\n"
        f"⚖️ Neutral Statements: {counts['neutral']}\n"
    )

    return report, "Sentiment Analysis Complete."
