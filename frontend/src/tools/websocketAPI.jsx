const WS_URL = "ws://127.0.0.1:8000/ws/controller-buttons/";

let activeSocket = null;

export const controllerEvents = (onData) => {
  activeSocket = new WebSocket(WS_URL);

  activeSocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onData(data);
    } catch (error) {
      console.error("Error parsing WS data:", error);
    }
  };

  activeSocket.onerror = (err) => console.error("WS Error:", err);

  return () => {
    if (
      activeSocket &&
      (activeSocket.readyState === WebSocket.OPEN ||
        activeSocket.readyState === WebSocket.CONNECTING)
    ) {
      activeSocket.close();
      activeSocket = null;
    }
  };
};

export const sendControllerEvent = (payload) => {
  if (activeSocket && activeSocket.readyState === WebSocket.OPEN) {
    activeSocket.send(JSON.stringify(payload));
    console.log("Sent via WS:", payload);
  } else {
    console.warn("WebSocket is not connected. Message dropped:", payload);
  }
};