import React, { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import './Message.css';
import AIIcon from '../../../images/artificial-intelligence.gif';
import MinervaIcon from '../../../images/icon.jpeg';
import Stack from '@mui/material/Stack';
import Skeleton from '@mui/material/Skeleton';
import MessageContent from './MessageContent';


const MessageComponent = ({ message, darkTheme, handleOpenErrorBar, handlePlaySpeak }) => {
    const id = message.id;
    const [isReviewed, setIsReviewed] = useState(false);

    const theme = darkTheme ? 'dark' : 'light';
    const src = message.actor === 'Bot' ? MinervaIcon : '.';
    const position = message.actor === 'Bot' ? 'flex-start' : 'flex-end';

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

    if (message.text !== "") {
        return (
            <Stack
                direction="row"
                justifyContent={position}
                alignItems={position}
                spacing={0}
            >
                <Stack
                    direction="row"
                    justifyContent="flex-start"
                    alignItems="flex-start"
                    spacing={0}
                    className={`Message scale-up-center ${theme}`}
                >
                    <Avatar alt={message.actor} src={src} sx={{ width: 36, height: 36 }} style={{marginRight: '8px'}}/>
                    <MessageContent
                        message={message}
                        isReviewed={isReviewed}
                        handlePlaySpeak={handlePlaySpeak}
                        handleThumbsUp={handleThumbsUp}
                        handleThumbsDown={handleThumbsDown}
                    />
                </Stack>
            </Stack>
        );
    } else {
        return (
            <Stack
                direction="row"
                justifyContent="flex-start"
                spacing={0}
                alignItems="flex-start"
            >
                <Stack
                    direction="row"
                    justifyContent="flex-start"
                    alignItems="flex-start"
                    spacing={1}
                    className={`LoadingMessage scale-up-center`}
                >
                    <Avatar alt="Minerva" src={AIIcon} sx={{ width: 36, height: 36 }} />
                    <div className='LinearProgressCenter'>
                        <Skeleton animation="wave" />
                        <Skeleton animation="wave" />
                        <Skeleton animation="wave" />
                        <Skeleton animation="wave" />
                    </div>
                </Stack>

            </Stack>
        );
    }
}

export default MessageComponent;