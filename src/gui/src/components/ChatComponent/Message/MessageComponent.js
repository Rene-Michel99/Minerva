import React, { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import './Message.css';
import MinervaIcon from '../../../images/icon.jpeg';
import IconButton from '@mui/material/IconButton';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import ExampleSnippet from './ExampleSnippet';


const MessageComponent = ({ message, handleOpenErrorBar, handlePlaySpeak }) => {
    const id = message.id;
    const [isReviewed, setIsReviewed] = useState(false);

    const className = message.actor === 'Bot' ? 'BotInput scale-up-center' : 'UserInput scale-up-center';
    const src = message.actor === 'Bot' ? MinervaIcon : '.';

    const reviewMessage = async (review) => {
        const url = 'http://localhost:8080/review';
    
        const options = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            id: id,
            feedback: review
          })
        };
    
        await fetch(url, options)
        .then((response) => {
          if(!response.ok) throw new Error(response.statusText);
          else return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.response.status){
                setIsReviewed(true);
            } else {
                handleOpenErrorBar("Message not found");      
            }
        })
        .catch(error => {
          handleOpenErrorBar(error.message);
          console.error(error.message);
        })
    }

    const handleThumbsUp = async () => {
        await reviewMessage(1);
    }
    
    const handleThumbsDown = async () => {
        await reviewMessage(0);
    }
    
    return (
        <div className={className}>
            <Avatar alt={message.actor} src={src} sx={{ width: 36, height: 36 }} style={{marginRight: '8px'}}/>
            <span>
                {message.text}
                {message.examples.map((example, index) => {
                    return <ExampleSnippet
                        key={message.id}
                        exampleText={example}
                        exampleLanguage={message.languages[index]}
                    />
                })}
                {message.actor === 'Bot' && (
                    <div>
                        <IconButton
                            size='small'
                            aria-label="speak"
                            onClick={() => handlePlaySpeak(message.text)}
                        ><VolumeUpIcon fontSize="inherit"/></IconButton>
                        {!isReviewed && (
                            <>
                                <IconButton
                                    size='small'
                                    aria-label="like"
                                    onClick={handleThumbsUp}
                                ><ThumbUpIcon fontSize="inherit"/></IconButton>
                                <IconButton
                                    size='small'
                                    aria-label="dislike"
                                    onClick={handleThumbsDown}
                                ><ThumbDownIcon fontSize="inherit"/></IconButton>
                            </>
                        )}
                    </div>
                )}
            </span>
        </div>
    );
}

export default MessageComponent;