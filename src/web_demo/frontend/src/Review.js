import React, { useState } from 'react';

function Review() {
  const [rating, setRating] = useState(0);
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleRating = (value) => {
    setRating(value);
  };

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleSubmit = () => {
    setSubmitted(true);
    // Here you can add logic to send the review to your backend
    setTimeout(() => setSubmitted(false), 2000);
  };

  return (
    <div style={{ marginTop: '30px', marginBottom: '30px', color: 'black' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px', fontSize: '18px' }}>
        <span style={{ marginRight: '16px' }}>Paraphrase review:</span>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          {[1,2,3,4,5].map((point) => (
            <span
              key={point}
              onClick={() => handleRating(point)}
              style={{
                cursor: 'pointer',
                fontSize: '32px',
                color: rating >= point ? 'black' : 'white',
                border: '2px solid black',
                borderRadius: '50%',
                marginRight: '10px',
                display: 'inline-block',
                width: '40px',
                height: '40px',
                textAlign: 'center',
                lineHeight: '36px',
                transition: 'color 0.2s, background 0.2s',
                background: rating >= point ? '#e0e0e0' : 'transparent'
              }}
            >
              ●
            </span>
          ))}
        </div>
      </div>
      <div style={{ marginBottom: '10px', fontSize: '18px' }}>Write your paraphrase</div>
      <textarea
        value={text}
        onChange={handleTextChange}
        rows={3}
        style={{
          width: '100%',
          border: '2px solid black',
          borderRadius: '4px',
          padding: '8px',
          fontSize: '16px',
          color: 'black',
          marginBottom: '10px',
          fontWeight: 'normal'
        }}
        placeholder="Write your paraphrase here..."
      />
      <br />
      <button
        onClick={handleSubmit}
        style={{
          background: (submitted || (rating === 0 && text.trim() === '')) ? '#cce2ff' : '#6ea8fe',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          padding: '8px 16px',
          fontWeight: 'bold',
          fontSize: '20px',
          cursor: (submitted || (rating === 0 && text.trim() === '')) ? 'not-allowed' : 'pointer',
          boxShadow: '0 2px 4px rgba(0,0,0,0.04)',
          transition: 'background 0.2s',
          opacity: 1,
        }}
        disabled={submitted || (rating === 0 && text.trim() === '')}
      >
        {submitted ? 'Submitted!' : 'Send Review'}
      </button>
    </div>
  );
}

export default Review;
