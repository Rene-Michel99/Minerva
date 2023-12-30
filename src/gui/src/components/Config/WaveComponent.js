import React from 'react';
import Wave from 'react-wavify';

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

const WaveComponent = ({isActive}) => {
  const height = isActive ? randomInt(0, 25) : 1;
  const points = isActive ? 10 : 2;
  const speed = isActive ? 5 : 0.5;

  return (
    <Wave
      fill='url(#gradient)'
      paused={false}
      //mask="url(#mask)"
      options={{
        height: height,
        amplitude: 150,
        speed: speed,
        points: points
      }}
    >
      <mask id="mask">
        <circle cx="50%" cy="50%" r="100" fill='white'/>
      </mask>
      <defs>
        <linearGradient id="gradient" gradientTransform="rotate(90)">
          <stop offset="10%"  stopColor="#44d2de" />
          <stop offset="90%" stopColor="#011337" />
        </linearGradient>
      </defs>
    </Wave>
  )
}

export default WaveComponent;
