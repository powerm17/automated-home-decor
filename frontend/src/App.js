import React, { useState } from 'react';
import axios from 'axios';
import { Button, Container, TextField, Typography, Card, CardMedia, CircularProgress } from '@mui/material';
import './App.css';

function App() {
  const [image, setImage] = useState(null);      // Store the selected image
  const [imagePreview, setImagePreview] = useState(null);  // Store the image preview
  const [response, setResponse] = useState(null);  // Store response from backend
  const [loading, setLoading] = useState(false);   // Handle loading state
  const [error, setError] = useState(null);        // Handle errors

  // Handle file input change
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);                      // Store the image file
      setImagePreview(URL.createObjectURL(file));  // Create preview URL for the image
    }
  };

  // Handle image upload
  const handleUpload = async () => {
    if (!image) {
      setError('Please select an image first');
      return;
    }
    setLoading(true);
    setError(null);  // Clear previous errors

    const formData = new FormData();
    formData.append('image', image);  // Append the image file to FormData

    try {
      // Post the image to Flask backend
      const res = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(res.data);  // Store the response
      setLoading(false);       // Stop loading spinner
    } catch (error) {
      setError('Error uploading image. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" style={{ padding: '20px', textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>Room Decor AI</Typography>

      {/* Image upload section */}
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleFileChange} 
        style={{ display: 'none' }} 
        id="image-upload" 
      />
      <label htmlFor="image-upload">
        <Button variant="contained" color="primary" component="span">
          Select Image
        </Button>
      </label>

      {/* Display image preview */}
      {imagePreview && (
        <Card style={{ marginTop: '20px', display: 'inline-block', maxWidth: '100%', maxHeight: '300px' }}>
          <CardMedia
            component="img"
            image={imagePreview}
            alt="Uploaded image preview"
            style={{ objectFit: 'contain' }}
          />
        </Card>
      )}

      {/* Error message */}
      {error && <Typography color="error" style={{ marginTop: '10px' }}>{error}</Typography>}

      {/* Button to upload the image */}
      <div style={{ marginTop: '20px' }}>
        <Button 
          variant="contained" 
          color="secondary" 
          onClick={handleUpload} 
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Upload Image'}
        </Button>
      </div>

      {/* Response */}
      {response && (
        <div style={{ marginTop: '30px' }}>
          <Typography variant="h6">AI Suggestions:</Typography>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </Container>
  );
}

export default App;
