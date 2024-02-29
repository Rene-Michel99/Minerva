import React, { useState, useRef, useEffect } from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import './ChatComponent.css';
import MessageComponent from './Message/MessageComponent.jsx';
import ErrorBar from './ErrorBar.jsx';
import uuidv4 from '../Utils.js';



const ChatComponent = ({voice, pitch, volume, rate, autoSpeak}) => {
    const [messages, setMessages] = useState([]);
    const [processing, setProcessing] = useState(false);
    const [openErrorBar, setopenErrorBar] = useState(false);
    const [errorMessage, setErrorMessage] = useState('error');
    const [utterance, setUtterance] = useState(null);
    const messagesEndRef = useRef(null);

    const handleProcessing = (value) => {
        setProcessing(value);
    }

    const handleNewMessage = (data) => {
        setMessages((previousMessages) => {
            const lastMessage = previousMessages[previousMessages.length - 1];
            if (lastMessage !== undefined && lastMessage.text === "" && lastMessage.actor === data.actor) {
                lastMessage.id = data.id;
                lastMessage.text = data.text;
                lastMessage.examples = data.examples;
                lastMessage.languages = data.languages;

                return previousMessages;
            } else {
                return [
                    ...previousMessages,
                    {
                        id: data.id,
                        actor: data.actor,
                        text: data.text,
                        examples: data.examples,
                        languages: data.languages
                    }
                ];
            }
        });
    }

    const handleDeleteMessage = () => {
        setMessages((previousMessages) => {
            previousMessages.pop();
            
            return previousMessages;
        });
    }
    
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    const handleOpenErrorBar = (errorMessage) => {
        setopenErrorBar(true);
        setErrorMessage(errorMessage);
    }

    const playAudio = async (responseText) => {
        const synth = window.speechSynthesis;
        utterance.text = responseText;
        utterance.voice = voice;
        utterance.pitch = pitch;
        utterance.rate = rate;
        utterance.volume = volume;
    
        synth.speak(utterance);
    }

    const handlePlaySpeak = async (responseText) => {
        await playAudio(responseText);
    };

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

        handleNewMessage({id: messageId, actor: "User", text: inputText, examples: [], languages: []});
        handleNewMessage({id: uuidv4(), actor: "Bot", text: "", examples: [], languages: []});
        handleProcessing(true);

        await fetch(url, options)
        .then((response) => {
            if(!response.ok) throw new Error(response.statusText);
            else return response.json();
        })
        .then(data => {
            handleCallAutoSpeak(data.text);
            handleNewMessage(data);
            
            const inputField = document.getElementById('userInput')
            inputField.value = "";
        })
        .catch(error => {
            handleDeleteMessage();
            handleProcessing(false);
            handleOpenErrorBar(error.message);
            console.error(error.message);
        })
    }

    useEffect(() => {
        const synth = window.speechSynthesis;
    
        const u = new SpeechSynthesisUtterance('');
        u.onend = () => {
            handleProcessing(false);
        };

        setUtterance(u);
        scrollToBottom();
        return () => {
            synth.cancel();
        };
    }, [messages]);

    return (
        <div className="Chat">
            <div className='Interactions'>
                {messages.map((message) => {
                    return (
                        <MessageComponent
                            key={message.id}
                            message={message}
                            handleOpenErrorBar={handleOpenErrorBar}
                            handlePlaySpeak={handlePlaySpeak}
                        />
                    )
                })}
                <div ref={messagesEndRef} />
            </div>
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
            <ErrorBar
                errorMessage={errorMessage}
                openErrorBar={openErrorBar}
                setopenErrorBar={setopenErrorBar}
            />
        </div>
    );
}

export default ChatComponent;