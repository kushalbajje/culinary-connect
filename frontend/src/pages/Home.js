import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Container, Grid, Typography, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import RecipeCard from '../components/RecipeCard';
import { getAllRecipes } from '../services/api';

const useStyles = makeStyles((theme) => ({
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
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
  noDataContainer: {
    textAlign: 'center',
    marginTop: theme.spacing(10),
  },
}));

const Home = () => {
  const classes = useStyles();
  const [recipesData, setRecipesData] = useState({
    results: [],
    count: 0,
    next: null,
    previous: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const loadMoreRef = useRef();

  const fetchRecipes = useCallback(async (url = null) => {
    setLoading(true);
    try {
      const data = await getAllRecipes(url);
      setRecipesData((prevData) => ({
        ...data,
        results: url
          ? [...prevData.results, ...data.results.filter(
              (newRecipe) => !prevData.results.some((recipe) => recipe.id === newRecipe.id)
            )]
          : data.results,
      }));
    } catch (error) {
      console.error('Failed to fetch recipes:', error);
      setError('Failed to load recipes. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRecipes();
  }, [fetchRecipes]);

  const handleLoadMore = useCallback(() => {
    if (recipesData.next && !loading) {
      fetchRecipes(recipesData.next);
    }
  }, [recipesData.next, loading, fetchRecipes]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && recipesData.next) {
          handleLoadMore();
        }
      },
      {
        root: null,
        rootMargin: '0px',
        threshold: 1.0,
      }
    );

    if (loadMoreRef.current) {
      observer.observe(loadMoreRef.current);
    }

    return () => {
      if (loadMoreRef.current) {
        observer.unobserve(loadMoreRef.current);
      }
    };
  }, [recipesData.next, handleLoadMore]);

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
        Discover Delicious Recipes
      </Typography>
      {recipesData.results.length === 0 ? (
        <div className={classes.noDataContainer}>
          <Typography variant="h6" color="textSecondary">
            No recipes found.
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Be the first to add a recipe or try refreshing the page.
          </Typography>
        </div>
      ) : (
        <>
          <Grid container spacing={4}>
            {recipesData.results.map((recipe) => (
              <Grid item key={recipe.id} xs={12} sm={6} md={6}>
                <RecipeCard recipe={recipe} />
              </Grid>
            ))}
          </Grid>
          <div ref={loadMoreRef} className={classes.paginationContainer}>
            {loading && <CircularProgress />}
          </div>
        </>
      )}
    </Container>
  );
};

export default Home;