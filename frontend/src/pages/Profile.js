import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, CircularProgress, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import RecipeCard from '../components/RecipeCard';
import { getUserRecipes } from '../services/api';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(4),
  },
  title: {
    marginBottom: theme.spacing(4),
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '50vh',
  },
  paginationContainer: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: theme.spacing(4),
  },
}));

const Profile = () => {
  const classes = useStyles();
  const [recipesData, setRecipesData] = useState({
    results: [],
    count: 0,
    next: null,
    previous: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchRecipes = async (url = null) => {
    setLoading(true);
    try {
      const data = await getUserRecipes(url);
      setRecipesData(data);
    } catch (error) {
      console.error('Failed to fetch user recipes:', error);
      setError('Failed to load your recipes. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecipes();
  }, []);

  const handleLoadMore = () => {
    if (recipesData.next) {
      fetchRecipes(recipesData.next);
    }
  };

  if (loading && recipesData.results.length === 0) {
    return (
      <Container className={classes.loadingContainer}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className={classes.container}>
        <Typography variant="h6" color="error" align="center">
          {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container className={classes.container}>
      <Typography variant="h4" component="h1" className={classes.title}>
        My Recipes
      </Typography>
      {recipesData.results.length === 0 ? (
        <Typography variant="body1" align="center">
          You haven't created any recipes yet. Start cooking!
        </Typography>
      ) : (
        <>
          <Grid container spacing={4}>
            {recipesData.results.map((recipe) => (
              <Grid item key={recipe.id} xs={12} sm={6} md={4}>
                <RecipeCard recipe={recipe} />
              </Grid>
            ))}
          </Grid>
          {recipesData.next && (
            <div className={classes.paginationContainer}>
              <Button variant="contained" color="primary" onClick={handleLoadMore} disabled={loading}>
                {loading ? 'Loading...' : 'Load More'}
              </Button>
            </div>
          )}
        </>
      )}
    </Container>
  );
};

export default Profile;