import React from 'react';
import { Button, Typography, Container, Box, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './HomePage.css'; 


const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm" style={{ padding: '40px', textAlign: 'center' }}>
      <Typography variant="h3" style={{ fontWeight: 'bold', color: '#333' }}>
        Welcome to Room Decor AI
      </Typography>
      <Typography variant="body1" paragraph style={{ marginTop: '20px', color: '#555' }}>
        Let us help you create the perfect ambiance for your space. Upload a picture and get personalized room decor suggestions!
      </Typography>
      
      {/* Call to Action */}
      <Box
        style={{
          marginTop: '30px',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/upload')}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#3f51b5',
            borderRadius: '30px',
          }}
        >
          Get Started
        </Button>
      </Box>

      {/* Optional: Add some design elements */}
      <Grid container spacing={3} style={{ marginTop: '40px' }}>
        <Grid item xs={12} sm={6}>
          <Paper style={{ padding: '20px', backgroundColor: '#f5f5f5', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
            <Typography variant="body1" style={{ fontWeight: 'bold' }}>
              Easy Upload
            </Typography>
            <Typography variant="body2" style={{ marginTop: '10px' }}>
              Upload an image of your space in just a few clicks.
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Paper style={{ padding: '20px', backgroundColor: '#f5f5f5', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
            <Typography variant="body1" style={{ fontWeight: 'bold' }}>
              Personalized Suggestions
            </Typography>
            <Typography variant="body2" style={{ marginTop: '10px' }}>
              Get decor ideas based on your image's colors and themes.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default HomePage;
