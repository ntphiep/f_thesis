import React from 'react';
import { Container, Row, Col } from 'reactstrap';

function Footer() {
  return (
    <div style={{
      position: 'fixed',
      right: 0,
      bottom: 0,
      width: 'auto',
      color: '#888',
      margin: '30px',
      fontWeight: 'normal',
      fontSize: '14px',
      zIndex: 1000,
      background: 'transparent',
      textAlign: 'right',
      pointerEvents: 'none'
    }}>
      F_thesis, by Hiep and Binh © 2025
    </div>
  );
}

export default Footer;
