import { useState, useEffect, useRef } from 'react';
import { get_button_cache } from '../tools/get';


const ITEMS = [
  { id: 'color1', label: 'Color 1', bg: 'bg-red-300', hex: '#fca5a5' },
  { id: 'color2', label: 'Color 2', bg: 'bg-blue-300', hex: '#93c5fd' },
  { id: 'color3', label: 'Color 3', bg: 'bg-green-300', hex: '#86efac' },
];

export default function ColorSelection({ onSelectColor }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [selectedColor, setSelectedColor] = useState(null);

  const selectedIndexRef = useRef(selectedIndex);
  useEffect(() => {
    selectedIndexRef.current = selectedIndex;
  }, [selectedIndex]);


  const handleConfirmSelection = (index) => {
    const chosenItem = ITEMS[index];
    setSelectedColor(chosenItem);
    console.log('Retrieved Color:', chosenItem);

    sendMessage({
      action: 'SELECT_COLOR',
      color: chosenItem,
    });

    if (onSelectColor) {
      onSelectColor(chosenItem);
    }
  };

  const prevTimeStampRef = useRef(null);

  useEffect(() => {
    const getButtonsCache = async () => {
      try {
        const buttonsData = await get_button_cache();
        // console.log(buttonsData?.[0]?.t)
        // print(buttonsData)

        if (buttonsData?.[0]?.t !== undefined) {
          const currentTimeStamp = buttonsData[0].t;

          if (
            prevTimeStampRef.current !== null &&
            currentTimeStamp !== prevTimeStampRef.current
          ) {
            console.log(buttonsData[0]);
          }

          prevTimeStampRef.current = currentTimeStamp;
        }
      } catch (error) {
        console.error("Error fetching buttons cache:", error);
      }
    };

    getButtonsCache();
    const intervalId = setInterval(getButtonsCache, 50);
    return () => clearInterval(intervalId);
  }, []);


  return (
    <div className='flex flex-col justify-center items-center gap-4'>
      <div className='flex flex-col w-full justify-center items-center gap-2'>
        {ITEMS.map((item, index) => {
          const isSelected = selectedIndex === index;

          return (
            <div
              key={item.id}
              onClick={() => {
                setSelectedIndex(index);
                handleConfirmSelection(index);
              }}
              className={`w-1/2 h-10 content-center text-center cursor-pointer font-bold ${item.bg} ${
                isSelected ? 'text-black outline-2 outline-black' : 'text-white'
              }`}
            >
              {item.label}
            </div>
          );
        })}
      </div>

      {selectedColor && (
        <div className='p-2 bg-gray-100 rounded border border-gray-300 text-center'>
          Retrieved: <span className='font-bold'>{selectedColor.label}</span> ({selectedColor.hex})
        </div>
      )}
    </div>
  );
}