#!/usr/bin/env python3
"""
Test script for reproducing and verifying fixes for the image processing bug.

This script tests the specific FontsInUse URL/image combination that caused
the delayed image display issue.
"""

import os
import sys
import json
import requests
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from io import BytesIO
import time

# Add the current directory to Python path to import app functions
sys.path.insert(0, os.path.dirname(__file__))

from app import download_and_process_image, fetch_url_metadata

class ImageProcessingTester:
    def __init__(self):
        self.test_url = "https://fontsinuse.com/uses/35835/the-arcane-alphabets-of-black-sabbath"
        self.test_image_url = "https://assets.fontsinuse.com/static/use-media-items/264/263609/upto-700xauto/68841a05/@2x/Black%20Sabbath%20titling.jpeg"
        self.temp_dir = None
        
    def setup(self):
        """Create temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp(prefix="image_test_")
        print(f"🔧 Test directory: {self.temp_dir}")
        
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up test directory")
    
    def test_metadata_extraction(self):
        """Test that we can extract metadata from the FontsInUse page"""
        print("\n📄 Testing metadata extraction...")
        
        try:
            metadata = fetch_url_metadata(self.test_url)
            
            if 'error' in metadata:
                print(f"❌ Metadata extraction failed: {metadata['error']}")
                return False
                
            print(f"✅ Title: {metadata.get('title', 'Not found')}")
            print(f"✅ Source: {metadata.get('source', 'Not found')}")
            print(f"✅ Images found: {len(metadata.get('images', []))}")
            
            # Check if our specific image is in the results
            if self.test_image_url in metadata.get('images', []):
                print(f"✅ Target image found in metadata")
                return True
            else:
                print(f"⚠️  Target image not found in initial metadata (this is expected)")
                return True
                
        except Exception as e:
            print(f"❌ Metadata extraction failed with exception: {e}")
            return False
    
    def test_image_download_success(self):
        """Test successful image download under normal conditions"""
        print("\n🖼️  Testing image download (normal conditions)...")
        
        try:
            filename = "test_image.jpg"
            image_data = download_and_process_image(self.test_image_url, filename)
            
            if image_data:
                print(f"✅ Image downloaded successfully ({len(image_data)} bytes)")
                
                # Save to temp file for verification
                test_file = os.path.join(self.temp_dir, filename)
                with open(test_file, 'wb') as f:
                    f.write(image_data)
                    
                print(f"✅ Image saved to: {test_file}")
                return True
            else:
                print("❌ Image download returned empty data")
                return False
                
        except Exception as e:
            print(f"❌ Image download failed: {e}")
            return False
    
    def test_image_download_with_timeout(self):
        """Test image download behavior when timeout occurs"""
        print("\n⏱️  Testing image download with timeout simulation...")
        
        # Mock requests.get to simulate timeout
        with patch('app.requests.get') as mock_get:
            # Simulate timeout exception
            mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
            
            try:
                filename = "test_image_timeout.jpg"
                image_data = download_and_process_image(self.test_image_url, filename)
                print("❌ Expected timeout exception but got successful response")
                return False
            except Exception as e:
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    print(f"✅ Timeout properly caught: {e}")
                    return True
                else:
                    print(f"❌ Unexpected exception: {e}")
                    return False
    
    def test_image_download_with_network_error(self):
        """Test image download behavior when network error occurs"""
        print("\n🚫 Testing image download with network error simulation...")
        
        # Mock requests.get to simulate connection error
        with patch('app.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network unreachable")
            
            try:
                filename = "test_image_network_error.jpg"
                image_data = download_and_process_image(self.test_image_url, filename)
                print("❌ Expected network error but got successful response")
                return False
            except Exception as e:
                if "network" in str(e).lower() or "connection" in str(e).lower():
                    print(f"✅ Network error properly caught: {e}")
                    return True
                else:
                    print(f"❌ Unexpected exception: {e}")
                    return False
    
    def test_post_creation_simulation(self):
        """Simulate the full post creation flow"""
        print("\n📝 Testing full post creation simulation...")
        
        test_data = {
            'title': 'The Arcane Alphabets of Black Sabbath',
            'url': self.test_url,
            'image': self.test_image_url,
            'content': 'Test post content',
            'source': 'FontsInUse'
        }
        
        print(f"📋 Simulating post creation with:")
        print(f"   - Title: {test_data['title']}")
        print(f"   - URL: {test_data['url']}")
        print(f"   - Image: {test_data['image']}")
        
        # This would test the full create_post flow in debug mode
        # For now, we'll just verify our components work
        try:
            # Test image processing
            image_data = download_and_process_image(test_data['image'], 'test_sabbath.jpg')
            
            if image_data:
                print("✅ Image processing successful in simulation")
                
                # Test front matter generation (simplified)
                front_matter = f'''---
title: "{test_data['title']}"
externalLink: "{test_data['url']}"
sourceUrl: "{test_data['source']}"
featuredImage: "/images/test_sabbath.jpg"
---'''
                print("✅ Front matter generated successfully")
                print(f"📄 Front matter preview:\n{front_matter}")
                return True
            else:
                print("❌ Image processing failed in simulation")
                return False
                
        except Exception as e:
            print(f"❌ Post creation simulation failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🚀 Starting Image Processing Bug Test Suite")
        print("=" * 60)
        
        self.setup()
        
        tests = [
            ("Metadata Extraction", self.test_metadata_extraction),
            ("Image Download (Success)", self.test_image_download_success),
            ("Image Download (Timeout)", self.test_image_download_with_timeout),
            ("Image Download (Network Error)", self.test_image_download_with_network_error),
            ("Post Creation Simulation", self.test_post_creation_simulation),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))
        
        self.cleanup()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        total = len(results)
        print(f"\n🏆 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The system is working correctly.")
        else:
            print("⚠️  Some tests failed. This indicates issues that need to be fixed.")
            
        return passed == total

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick test - just the real image download
        tester = ImageProcessingTester()
        tester.setup()
        success = tester.test_image_download_success()
        tester.cleanup()
        sys.exit(0 if success else 1)
    else:
        # Full test suite
        tester = ImageProcessingTester()
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()