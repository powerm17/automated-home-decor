import React, { useState } from 'react';
import axios from 'axios';
import {
  Button,
  Container,
  Typography,
  Card,
  CardMedia,
  CircularProgress,
  Grid,
  Box,
  Snackbar,
  Tooltip,
  Paper,
} from '@mui/material';
import './App.css'; // If you haven't already added this

const MainPage = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  // Handle image file change
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file));  // Display image preview
    }
  };

  // Handle image upload
  const handleUpload = async () => {
    if (!image) {
      setError('Please select an image first');
      return;
    }
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('image', image);

    try {
      const res = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResponse(res.data);  // Set the response from the backend
      setLoading(false);
      setOpenSnackbar(true);  // Show success message
    } catch (error) {
      setError('Error uploading image. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" style={{ padding: '20px', textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom style={{ fontWeight: 600, color: '#333' }}>
        Room Decor AI
      </Typography>
      <Typography variant="body1" paragraph>
        Upload an image to receive personalized room decor suggestions. Let us help you design a beautiful space!
      </Typography>

      {/* Image upload section */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="image-upload"
      />
      <label htmlFor="image-upload">
        <Tooltip title="Select an image to upload" placement="top">
          <Button variant="contained" color="primary" component="span">
            Select Image
          </Button>
        </Tooltip>
      </label>

      {/* Display image preview */}
      {imagePreview && (
        <Card style={{ marginTop: '20px', display: 'inline-block', width: '100%' }}>
          <CardMedia
            component="img"
            image={imagePreview}
            alt="Uploaded Image"
            style={{ height: 'auto', maxWidth: '100%', objectFit: 'contain' }}
          />
        </Card>
      )}

      {/* Handle loading state */}
      {loading && <CircularProgress style={{ marginTop: '20px' }} />}

      {/* Button to trigger the upload */}
      <div style={{ marginTop: '20px' }}>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpload}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Upload Image'}
        </Button>
      </div>

      {/* Display response data */}
      {response && (
        <Box style={{ marginTop: '20px' }}>
          <Typography variant="h6" style={{ fontWeight: 600 }}>
            Suggested Items:
          </Typography>
          <Grid container spacing={2}>
          {Object.entries(response.suggestions).map(([item, suggestions]) => (
            <Grid item xs={12} sm={6} key={item}>
              <Paper style={{ padding: '10px', marginBottom: '10px' }}>
                <Typography variant="body1" style={{ fontWeight: 'bold' }}>
                  {item}
                </Typography>
                {suggestions.length > 0 ? (
                  suggestions.map((suggestion, index) => (
                    <Typography key={index} variant="body2">
                      {suggestion}
                    </Typography>
                  ))
                ) : (
                  <Typography variant="body2">No suggestions available</Typography>
                )}
              </Paper>
            </Grid>
          ))}
          </Grid>

          {/* Display prominent colors */}
          <Typography variant="h6" style={{ marginTop: '20px', fontWeight: 600 }}>
            Prominent Colors:
          </Typography>
          <Grid container spacing={1}>
            {response.prominent_colors.map((color, index) => (
              <Grid item key={index}>
                <Box
                  style={{
                    backgroundColor: color,
                    width: '50px',
                    height: '50px',
                    borderRadius: '5px',
                  }}
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Display error message */}
      {error && (
        <Typography color="error" variant="body1" style={{ marginTop: '20px' }}>
          {error}
        </Typography>
      )}

      {/* Snackbar for success message */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={() => setOpenSnackbar(false)}
        message="Image uploaded successfully!"
      />
    </Container>
  );
};

export default MainPage;

