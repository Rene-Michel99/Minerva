import React from 'react';
import Stack from '@mui/material/Stack';
import Skeleton from '@mui/material/Skeleton';
import Avatar from '@mui/material/Avatar';
import MinervaIcon from '../../../images/icon.jpeg';
import AIIcon from '../../../images/artificial-intelligence.gif';
import './Message.css';


const LoadingMessage = ({ darkTheme }) => {
    const theme = darkTheme ? 'dark' : 'light';

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
                className={`LoadingMessage scale-up-center ${theme}`}
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

export default LoadingMessage;