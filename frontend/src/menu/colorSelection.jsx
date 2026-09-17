import { useState, useEffect } from "react";
import { controllerEvents, sendControllerEvent } from "../tools/websocketAPI";

const ITEMS = [
	{ id: "color1", label: "red", hex: "#ff0000", bg: "bg-red-600", text: "text-red-600" },
	{ id: "color2", label: "green", hex: "#00ff00", bg: "bg-green-500", text: "text-green-500" },
	{ id: "color3", label: "blue", hex: "#0000ff", bg: "bg-blue-600", text: "text-blue-600" },
	{ id: "color4", label: "white", hex: "#ffffff", bg: "bg-white", text: "text-slate-900" },
	{ id: "color5", label: "reset", hex: "#000000", bg: "bg-black", text: "text-black" },
];

const ACCEPT_BUTTON_INDEX = ITEMS.length;

export default function ColorSelector({ onSelectColor }) {
	const [selectedIndex, setSelectedIndex] = useState(0);
	const [focusedIndex, setFocusedIndex] = useState(0);

	const handleConfirmSelection = (index) => {
		const chosenItem = ITEMS[index];

		sendControllerEvent({
			action: "SELECT_COLOR",
			color: chosenItem,
			timestamp: new Date().toISOString(),
		});

		if (onSelectColor) {
			onSelectColor(chosenItem);
		}
	};

	useEffect(() => {
		const cleanup = controllerEvents((controllerData) => {
			if (controllerData?.type !== "button") return;

			const buttonName = controllerData.name;
			const totalElements = ITEMS.length + 1;

			if (buttonName === "TB") {
				setFocusedIndex((prev) => (prev + 1) % totalElements);
			} else if (buttonName === "TF") {
				setFocusedIndex((prev) => (prev - 1 + totalElements) % totalElements);
			} else if (buttonName === "A") {
				setFocusedIndex((currentFocus) => {
					if (currentFocus === ACCEPT_BUTTON_INDEX) {
						handleConfirmSelection(selectedIndex);
						return currentFocus;
					} else {
						setSelectedIndex(currentFocus);
						return ACCEPT_BUTTON_INDEX;
					}
				});
			}
		});

		return () => cleanup && cleanup();
	}, [selectedIndex]);

	const isAcceptFocused = focusedIndex === ACCEPT_BUTTON_INDEX;

	return (
		<div className="flex flex-col w-full justify-center items-center gap-4">
			<div className="flex flex-col w-1/3 justify-center gap-2">
				<div className="flex w-min items-center content-start justify-start h-10 border-2">
          Previous
        </div>
				{ITEMS.map((item, index) => {
					const isSelected = selectedIndex === index;
					const isFocused = focusedIndex === index;

					return (
						<div
							key={item.id}
							onClick={() => {
								setSelectedIndex(index);
								setFocusedIndex(index);
							}}
							className={`w-full h-10 content-center text-center cursor-pointer font-bold transition-all bg-white ${isSelected ? `font-extrabold text-black` : `text-black`} ${isFocused ? `ring-4 ring-yellow-400 scale-105 ${item.text}` : `text-black bg-black/50!`}`}
						>
							{item.label}
						</div>
					);
				})}

				<button
					onClick={() => {
						setFocusedIndex(ACCEPT_BUTTON_INDEX);
						handleConfirmSelection(selectedIndex);
					}}
					className={`w-full h-10 text-black border-2 font-bold rounded cursor-pointer transition-all ${isAcceptFocused ? "ring-4 ring-yellow-400 scale-105 bg-black text-white" : ""}`}
				>
					Accept & Send
				</button>
			</div>
		</div>
	);
}
