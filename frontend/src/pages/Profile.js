import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid } from '@material-ui/core';
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
}));

const Profile = () => {
  const classes = useStyles();
  const [userRecipes, setUserRecipes] = useState([]);

  useEffect(() => {
    const fetchUserRecipes = async () => {
      try {
        const recipes = await getUserRecipes();
        setUserRecipes(recipes);
      } catch (error) {
        console.error('Failed to fetch user recipes:', error);
      }
    };

    fetchUserRecipes();
  }, []);

  return (
    <Container className={classes.container}>
      <Typography variant="h4" component="h1" className={classes.title}>
        My Recipes
      </Typography>
      <Grid container spacing={4}>
        {userRecipes.map((recipe) => (
          <Grid item key={recipe.id} xs={12} sm={6} md={4}>
            <RecipeCard recipe={recipe} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Profile;