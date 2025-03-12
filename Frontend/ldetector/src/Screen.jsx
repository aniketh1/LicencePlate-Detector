import React from 'react'

function Screen() {
  return (
    <div className='relative h-screen w-screen'>
      <img 
        className='h-full w-full object-cover absolute z-0' 
        src="https://www.cars24.com/article/_next/image/?url=https%3A%2F%2Fcdn.cars24.com%2Fprod%2Fauto-news24-cms%2Froot%2F2024%2F07%2F23%2Fd62861af-324a-49a0-84b1-18c9a521d3fb-VIP-Number-Plate-Price-for-Cars_-Fancy-Number-Plate-(4)-(1).jpg&w=750&q=50" 
        alt="Background" 
      />

      <div className='absolute inset-0 flex items-center justify-center text-center h-full bg-black bg-opacity-70 w-full z-10 px-4'>
        <p className='text-white text-2xl sm:text-2xl md:text-3xl lg:text-4xl font-bold  p-6 rounded-lg shadow-lg'>
          "Empowering smarter roads and seamless security through cutting-edge technology, our License Plate Detector leverages AI-driven precision and real-time tracking to revolutionize vehicle identification. Designed for reliability and scalability, it is the perfect solution for modern traffic management, secure parking systems, and intelligent transport networks."
        </p>
      </div>
    </div>
  )
}

export default Screen
