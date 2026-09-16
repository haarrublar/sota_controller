import { useEffect, useState, useCallback, useRef } from 'react';

export function UseControllerAPI(url = 'ws://localhost:8765') {
  const [controllerData, setControllerData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setControllerData(data);
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    ws.onerror = (err) => console.error('WS error', err);

    ws.onclose = () => {
      console.log('disconnected');
      setIsConnected(false);
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [url]);

    const sendMessage = useCallback((data) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify(data));
        } else {
        console.warn('WebSocket is not connected');
        }
    }, []);  

  return { controllerData, isConnected, sendMessage };
}