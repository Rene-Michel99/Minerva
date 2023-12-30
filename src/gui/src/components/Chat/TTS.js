import React from "react";
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import SendIcon from '@mui/icons-material/Send';
import uuidv4 from '../Utils.js';


const TextToSpeech = ({
  text, processing, autoSpeak, handlePlaySpeak, handleInputChange, handleNewMessage,
  handleProcessing, handleWaitingMessage, handleOpenErrorBar
}) => {

  const handleCallAutoSpeak = (responseText) => {
    if (autoSpeak) {
      handlePlaySpeak(responseText);
    } else {
      handleProcessing(false);
    }
  }

  const sendMessage = async () => {
    const url = 'http://localhost:8080/inference';
    const messageId = uuidv4();

    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        id: messageId,
        sentence: text
      })
    };

    console.log(text);
    if (text === '') {
      return;
    }
    
    handleNewMessage('User', text, messageId);
    handleProcessing(true);
    handleWaitingMessage(true);

    await fetch(url, options)
    .then((response) => {
      if(!response.ok) throw new Error(response.statusText);
      else return response.json();
    })
    .then(data => {
      console.log(data);
      const responseText = data.text !== '. . .' ? data.text : 'não sei';
      
      handleCallAutoSpeak(responseText);

      handleWaitingMessage(false);
      handleNewMessage('Bot', responseText, data.id);
      
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
        <TextField
          id="inputText"
          variant="outlined"
          onChange={handleInputChange}
          style={{width: '90%'}}
        />
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