import React from "react";
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import SendIcon from '@mui/icons-material/Send';
import uuidv4 from '../Utils.js';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import "./ChatComponent.css";


const TextToSpeech = ({
  processing, autoSpeak, darkTheme, handlePlaySpeak, handleNewMessage,
  handleProcessing, handleWaitingMessage, handleOpenErrorBar
}) => {

  const handleCallAutoSpeak = (responseText) => {
    if (autoSpeak) {
      handlePlaySpeak(responseText);
    } else {
      handleProcessing(false);
    }
  }
  
  const theme = createTheme({
    components: {
      MuiInputBase: {
        styleOverrides: {
          input: {
            color: darkTheme ? '#ECECEC' : 'inherit',
          },
        },
      },
    },
  });

  const sendMessage = async () => {
    const url = 'http://localhost:8080/inference';
    const messageId = uuidv4();
    const inputText = document.getElementById('inputText').value;

    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        id: messageId,
        sentence: inputText
      })
    };

    if (inputText === '') {
      return;
    }
    
    handleNewMessage('User', {id: messageId, text: inputText, examples: [], languages: []});
    handleProcessing(true);
    handleWaitingMessage(true);

    await fetch(url, options)
    .then((response) => {
      if(!response.ok) throw new Error(response.statusText);
      else return response.json();
    })
    .then(data => {      
      handleCallAutoSpeak(data.text);

      handleWaitingMessage(false);
      handleNewMessage('Bot', data);
      
      const inputField = document.getElementById('inputText')
      inputField.value = "";
    })
    .catch(error => {
      handleWaitingMessage(false);
      handleProcessing(false);
      handleOpenErrorBar(error.message);
      console.error(error.message);
    })
  }
  

  return (
    <div style={{ padding: '12px' }}>
      <Stack direction="row" spacing={2}>
        <ThemeProvider theme={theme}>
          <TextField
            id="inputText"
            variant="outlined"
            style={{width: '90%', color: 'white'}}
            focused={darkTheme}
          />
        </ThemeProvider>
        <Button
          variant="contained"
          onClick={sendMessage}
          endIcon={<SendIcon />}
          disabled={processing}
        >Send</Button>
      </Stack>
    </div>
  );
};

export default TextToSpeech;