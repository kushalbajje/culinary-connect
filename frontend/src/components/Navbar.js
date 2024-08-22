import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, IconButton, Hidden, Drawer, List, ListItem, ListItemText } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import { AuthContext } from '../App';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    title: {
        flexGrow: 1,
        color: 'inherit', // Ensure the title text color matches the AppBar text color
        textDecoration: 'none', // Remove underline from link
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    list: {
        width: 250,
    },
}));

const Navbar = () => {
    const classes = useStyles();
    const navigate = useNavigate();
    const { user, logout } = useContext(AuthContext);
    const [drawerOpen, setDrawerOpen] = React.useState(false);

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }
        setDrawerOpen(open);
    };

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };

    const drawer = (
        <div
            className={classes.list}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
        >
            <List>
                <ListItem button component={Link} to="/">
                    <ListItemText primary="Home" />
                </ListItem>
                {user ? (
                    <>
                        <ListItem button component={Link} to="/create-recipe">
                            <ListItemText primary="Create Recipe" />
                        </ListItem>
                        <ListItem button component={Link} to="/profile">
                            <ListItemText primary="Profile" />
                        </ListItem>
                        <ListItem button onClick={handleLogout}>
                            <ListItemText primary="Logout" />
                        </ListItem>
                    </>
                ) : (
                    <>
                        <ListItem button component={Link} to="/login">
                            <ListItemText primary="Login" />
                        </ListItem>
                        <ListItem button component={Link} to="/register">
                            <ListItemText primary="Register" />
                        </ListItem>
                    </>
                )}
            </List>
        </div>
    );

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <Hidden smUp>
                        <IconButton
                            edge="start"
                            className={classes.menuButton}
                            color="inherit"
                            aria-label="menu"
                            onClick={toggleDrawer(true)}
                        >
                            <MenuIcon />
                        </IconButton>
                    </Hidden>
                    <Typography
                        variant="h4"
                        component={Link}
                        to="/"
                        className={classes.title}
                    >
                        Culinary Connect
                    </Typography>
                    <Hidden xsDown>
                        <Button color="inherit" component={Link} to="/">
                            Home
                        </Button>
                        {user ? (
                            <>
                                <Button color="inherit" component={Link} to="/create-recipe">
                                    Create Recipe
                                </Button>
                                <Button color="inherit" component={Link} to="/profile">
                                    Profile
                                </Button>
                                <Button color="inherit" onClick={handleLogout}>
                                    Logout
                                </Button>
                            </>
                        ) : (
                            <>
                                <Button color="inherit" component={Link} to="/login">
                                    Login
                                </Button>
                                <Button color="inherit" component={Link} to="/register">
                                    Register
                                </Button>
                            </>
                        )}
                    </Hidden>
                </Toolbar>
            </AppBar>
            <Drawer open={drawerOpen} onClose={toggleDrawer(false)}>
                {drawer}
            </Drawer>
        </div>
    );
};

export default Navbar;
