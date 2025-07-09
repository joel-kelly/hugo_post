# Image Upload Bug Fix

## Problem
When creating posts with featured images, the images were uploaded to the GitHub repository but the `featuredImage` field was not being added to the post's front matter.

## Root Cause
The issue was in the `create_post()` function in `app.py`:

1. **Variable Scope Issue**: The `image_data` variable was only defined inside the `if not DEBUG_MODE:` block, but the upload logic was checking for it in the broader scope.

2. **Incorrect Scope Check**: The upload logic was using `'image_data' in locals()` which could fail due to variable scope issues.

## Fix Applied
1. **Moved variable declaration**: Declared `image_data = None` at the beginning of the function to ensure proper scope.

2. **Simplified condition**: Changed the upload condition from `if image_filename and 'image_data' in locals():` to `if image_filename and image_data:`.

3. **Added debug logging**: Added print statements to help diagnose future issues:
   - Log when processing posts with images
   - Log when images are created vs already exist
   - Log warnings when image processing fails

## Code Changes
```python
# Before (buggy):
if data.get('image'):
    if not DEBUG_MODE:
        image_data = download_and_process_image(data['image'], image_filename)
    # ... later ...
    if image_filename and 'image_data' in locals():
        # Upload logic

# After (fixed):
image_data = None
if data.get('image'):
    if not DEBUG_MODE:
        image_data = download_and_process_image(data['image'], image_filename)
    # ... later ...
    if image_filename and image_data:
        # Upload logic
```

## Testing
The fix has been deployed and should now correctly:
1. Process and download the selected image
2. Add the `featuredImage: "/images/filename.ext"` field to the post front matter
3. Upload the image to the `static/images/` directory in the repository

## Next Steps
Test the fix by creating a new post with an image to verify both the markdown file and image are properly linked.