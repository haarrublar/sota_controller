import React, { useEffect, useRef } from 'react';

export default function ControllerAPI() {
  // const prevButtonsRef = useRef([]);

  // useEffect(() => {
  //   let frame;
  //   const DEADZONE = 0.1;

  //   const onConnect = (e) => {
  //     console.log('Gamepad connected:', e.gamepad.id, e.gamepad.index);
  //   };
  //   const onDisconnect = (e) => {
  //     console.log('Gamepad disconnected:', e.gamepad.id);
  //   };
  //   window.addEventListener('gamepadconnected', onConnect);
  //   window.addEventListener('gamepaddisconnected', onDisconnect);

  //   const status = () => {
  //     const gamepads = navigator.getGamepads();
  //     const gamecontroller = Array.from(gamepads).find(gp => gp && gp.connected);

  //     if (gamecontroller) {
  //       gamecontroller.buttons.forEach((btn, i) => {
  //         const wasPressed = prevButtonsRef.current[i] || false;

  //         if (btn.pressed && !wasPressed) {
  //           console.log(`Button ${i} pressed`);   // fires once, on press
  //         }
  //         if (!btn.pressed && wasPressed) {
  //           console.log(`Button ${i} released`);  // fires once, on release
  //         }

  //         prevButtonsRef.current[i] = btn.pressed;
  //       });

  //       gamecontroller.axes.forEach((value, i) => {
  //         if (Math.abs(value) > DEADZONE) {
  //           console.log(`Axis ${i}: ${value.toFixed(3)}`);
  //         }
  //       });
  //     }
  //     frame = requestAnimationFrame(status);
  //   };

  //   status();

  //   return () => {
  //     cancelAnimationFrame(frame);
  //     window.removeEventListener('gamepadconnected', onConnect);
  //     window.removeEventListener('gamepaddisconnected', onDisconnect);
  //   };
  // }, []);

  return <div>Hello</div>;
}