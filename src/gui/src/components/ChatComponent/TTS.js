import React from "react";
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import uuidv4 from '../Utils.js';
import "./ChatComponent.css";


const TextToSpeech = ({
  processing, autoSpeak, handlePlaySpeak, handleNewMessage,
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
    const inputText = document.getElementById('userInput').value;

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
        <input id="userInput" type="text" className="Input-text"></input>
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