
import requests
import os
import random
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from groq import Groq

def generate_pisces_memes_with_ai(count=5):
    """
    Generate fresh Pisces meme texts using Groq AI (FREE!)
    """
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("⚠️ GROQ_API_KEY not found, using fallback memes")
        return get_fallback_memes(count), get_fallback_caption()
    
    try:
        client = Groq(api_key=api_key)
        
        # Generate meme texts
        meme_prompt = f"""Generate {count} funny, relatable Pisces zodiac meme texts. Each should be:
- 1-3 short lines (max 10 words per line)
- About Pisces personality traits (emotional, daydreaming, avoidant, sensitive, intuitive, etc)
- Humorous and self-deprecating
- Format: exactly one meme per line, separated by blank lines
- No numbering, no bullets, just the text

Examples:
Pisces: cries in the shower
so no one can tell

Pisces avoiding confrontation
like it's their job

POV: Pisces just felt
a vibe shift

Now generate {count} NEW unique Pisces memes:"""

        meme_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": meme_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=1.0,
            max_tokens=500,
        )
        
        # Parse meme response
        response_text = meme_completion.choices[0].message.content.strip()
        memes = [meme.strip() for meme in response_text.split('\n\n') if meme.strip()]
        memes = [meme.split('. ', 1)[-1] if '. ' in meme[:5] else meme for meme in memes]
        
        # If we got fewer than requested, add fallbacks
        if len(memes) < count:
            memes.extend(get_fallback_memes(count - len(memes)))
        
        print(f"✨ Generated {len(memes)} fresh AI memes")
        
        # Generate Instagram caption
        caption_prompt = """Generate a short, engaging Instagram caption for a Pisces zodiac meme carousel post. 
Requirements:
- Keep it under 100 characters
- Use 2-3 relevant emojis (pisces ♓️, fish 🐟, water 💙, etc)
- Include 3-5 hashtags: #pisces #zodiac #astrology and similar
- Make it relatable and funny
- Examples: "why am I like this 😭 #pisces #zodiac #memes" or "pisces energy today ♓️💙 #astrology #relatable"

Generate ONE caption:"""

        caption_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": caption_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=1.2,
            max_tokens=100,
        )
        
        caption = caption_completion.choices[0].message.content.strip()
        # Remove quotes if AI added them
        caption = caption.strip('"\'')
        
        print(f"✨ Generated caption: {caption[:50]}...")
        
        return memes[:count], caption
        
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        print("Using fallback memes instead")
        return get_fallback_memes(count), get_fallback_caption()

def get_fallback_caption():
    """Fallback caption if AI fails"""
    captions = [
        "why am I like this 😭 #pisces #zodiac #astrology #memes",
        "pisces things ♓️ #piscesseason #zodiacmemes #astrologymemes",
        "tag a pisces 🐟 #pisces #zodiacsigns #horoscope",
        "POV: you're a pisces #astrology #pisces #relatable",
        "pisces energy 💙 #zodiac #pisces #meme",
    ]
    return random.choice(captions)

def get_fallback_memes(count=5):
    """Fallback memes if AI fails"""
    fallback = [
        "Pisces: cries in the shower\nso no one can tell",
        "POV: Pisces just felt\na vibe shift",
        "Pisces avoiding confrontation\nlike it's their job",
        "Pisces: I'm fine\n(currently having an\nexistential crisis)",
        "Pisces ghosting everyone\nincluding themselves",
        "Pisces processing emotions\nat 3am",
        "Pisces overthinking a\nconversation from 2019",
        "Pisces: too empathetic\nfor this world",
        "Pisces disappearing\nfor no reason",
        "Pisces living in their\nhead rent free",
    ]
    return random.sample(fallback, min(count, len(fallback)))

def create_meme_image(text, output_path):
    """
    Create a simple black text on white background meme
    """
    # Image dimensions (Instagram square)
    width = 1080
    height = 1080
    
    # Create white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a bold font, fallback to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
            print("Warning: Using default font.")
    
    # Split text into lines
    lines = text.split('\n')
    
    # Calculate total text height
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_height = sum(line_heights) + (len(lines) - 1) * 20
    
    # Start position (centered vertically)
    y = (height - total_height) // 2
    
    # Draw each line centered
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), line, fill='black', font=font)
        y += bbox[3] + 20
    
    # Save image
    img.save(output_path, 'PNG')
    print(f"✓ Created: {output_path}")
    return output_path

def upload_to_imgbb(image_path):
    """
    Upload image to ImgBB (free image hosting)
    Returns the direct image URL
    """
    api_key = os.getenv('IMGBB_API_KEY')
    
    if not api_key:
        print("❌ IMGBB_API_KEY not found in secrets")
        return None
    
    url = "https://api.imgbb.com/1/upload"
    
    with open(image_path, 'rb') as f:
        import base64
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        'key': api_key,
        'image': image_data,
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        image_url = response.json()['data']['url']
        print(f"✓ Uploaded: {image_url}")
        return image_url
    else:
        print(f"✗ ImgBB upload failed: {response.text}")
        return None

def create_instagram_media_container(image_url, access_token, account_id, is_carousel_item=False):
    """Create Instagram media container for a single image"""
    url = f"https://graph.facebook.com/v18.0/{account_id}/media"
    
    params = {
        'image_url': image_url,
        'access_token': access_token
    }
    
    # If this is a carousel item, mark it as such
    if is_carousel_item:
        params['is_carousel_item'] = 'true'
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        container_id = response.json().get('id')
        print(f"✓ Container created: {container_id}")
        return container_id
    else:
        print(f"✗ Error creating container: {response.text}")
        return None

def create_carousel_container(media_ids, caption, access_token, account_id):
    """Create a carousel container with multiple images"""
    url = f"https://graph.facebook.com/v18.0/{account_id}/media"
    
    params = {
        'media_type': 'CAROUSEL',
        'children': ','.join(media_ids),
        'caption': caption,
        'access_token': access_token
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        carousel_id = response.json().get('id')
        print(f"✓ Carousel container created: {carousel_id}")
        return carousel_id
    else:
        print(f"✗ Error creating carousel: {response.text}")
        return None

def publish_instagram_post(container_id, access_token, account_id, max_retries=5):
    """Publish the Instagram post with retry logic"""
    url = f"https://graph.facebook.com/v18.0/{account_id}/media_publish"
    
    params = {
        'creation_id': container_id,
        'access_token': access_token
    }
    
    import time
    
    for attempt in range(max_retries):
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            post_id = response.json().get('id')
            print(f"✅ Successfully posted carousel to Instagram! Post ID: {post_id}")
            return post_id
        else:
            error_data = response.json()
            error_code = error_data.get('error', {}).get('code')
            
            # Error 9007 means media is still processing - wait and retry
            if error_code == 9007 and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10  # 10s, 20s, 30s, etc
                print(f"⏳ Media still processing, waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                time.sleep(wait_time)
                continue
            else:
                print(f"❌ Error publishing post: {response.text}")
                return None
    
    print(f"❌ Failed to publish after {max_retries} attempts")
    return None

def main():
    """Main function"""
    print("🎨 Generating 5 fresh AI-powered Pisces memes...")
    
    # Get Instagram credentials
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    if not access_token or not account_id:
        print("❌ Missing Instagram credentials")
        print("Add INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_ACCOUNT_ID to GitHub secrets")
        return
    
    # Generate fresh memes and caption using AI
    selected_memes, caption = generate_pisces_memes_with_ai(5)
    
    image_urls = []
    media_container_ids = []
    
    # Generate and upload each image
    for i, meme_text in enumerate(selected_memes, 1):
        print(f"\n📄 Processing meme {i}/5...")
        print(f"Text: {meme_text[:50]}...")
        
        # Create image
        image_path = f'meme_{i}.png'
        create_meme_image(meme_text, image_path)
        
        # Upload to ImgBB
        print(f"📤 Uploading image {i}...")
        image_url = upload_to_imgbb(image_path)
        
        if not image_url:
            print(f"❌ Failed to upload image {i}")
            return
        
        image_urls.append(image_url)
        
        # Create Instagram media container for this image
        print(f"📸 Creating Instagram container {i}...")
        container_id = create_instagram_media_container(
            image_url, 
            access_token, 
            account_id, 
            is_carousel_item=True
        )
        
        if not container_id:
            print(f"❌ Failed to create container for image {i}")
            return
        
        media_container_ids.append(container_id)
        
        # Small delay to avoid rate limits
        import time
        time.sleep(1)
    
    print(f"\n🎠 Creating carousel with {len(media_container_ids)} images...")
    
    # Create carousel container
    carousel_id = create_carousel_container(
        media_container_ids,
        caption,
        access_token,
        account_id
    )
    
    if not carousel_id:
        print("❌ Failed to create carousel container")
        return
    
    # Wait for Instagram to process the media
    print("⏳ Waiting 15 seconds for Instagram to process media...")
    import time
    time.sleep(15)
    
    # Publish the carousel
    print("🚀 Publishing carousel to Instagram...")
    publish_instagram_post(carousel_id, access_token, account_id)
    
    print("\n✨ Done! Check your Instagram account.")

if __name__ == "__main__":
    main()
