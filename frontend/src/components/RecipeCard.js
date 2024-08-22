import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Card, CardActionArea, CardContent, CardMedia, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  root: {
    maxWidth: '100%',  // Make sure it takes full width within its container
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', // Add a box shadow
    transition: '0.3s',  // Smooth transition for hover effect
    '&:hover': {
      boxShadow: '0 8px 16px rgba(0, 0, 0, 0.3)',  // Increase shadow on hover
      transform: 'translateY(-4px)',  // Move the card upwards on hover
    },
  },
  media: {
    height: 300,
  },
});

const RecipeCard = ({ recipe }) => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardActionArea component={RouterLink} to={`/recipe/${recipe.id}`}>
        <CardMedia
          className={classes.media}
          image={recipe.image || 'https://via.placeholder.com/345x140.png?text=No+Image'}
          title={recipe.title}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {recipe.title}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            {recipe.description}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Difficulty: {recipe.difficulty}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Preparation Time: {recipe.preparation_time} minutes
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default RecipeCard;