import React from 'react';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/Button';


const ErrorBar = ({ errorMessage, openErrorBar, setopenErrorBar }) => {

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setopenErrorBar(false);
  };
  const action = (
      <React.Fragment>
        <Button color="secondary" size="small" onClick={handleClose}>
          UNDO
        </Button>
        <IconButton
          size="small"
          aria-label="close"
          color="inherit"
          onClick={handleClose}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      </React.Fragment>
    );

    return (
        <Snackbar
            open={openErrorBar}
            autoHideDuration={6000}
            onClose={handleClose}
            message={errorMessage}
            action={action}
            severity="error"
        />
    )
}

export default ErrorBar;