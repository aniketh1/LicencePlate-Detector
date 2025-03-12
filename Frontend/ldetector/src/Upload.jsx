import React, { useState } from 'react';
import './Global.css';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [outputFile, setOutputFile] = useState(null);
    const [licensePlate, setLicensePlate] = useState(null);
    const [processing, setProcessing] = useState(false);

    // Handle file upload
    const handleFileUpload = (e) => {
        const uploadedFile = e.target.files[0];
        const allowedTypes = ['image/jpeg', 'image/png', 'video/mp4', 'video/webm'];  // Supported file types
        
        if (uploadedFile && !allowedTypes.includes(uploadedFile.type)) {
            alert('Invalid file type. Please upload an image or video.');
            setFile(null); // Reset file selection if invalid type
        } else {
            setFile(uploadedFile);
            setLicensePlate(null);  // Reset license plate when a new file is selected
            setOutputFile(null);  // Reset previous output file
        }
    };

    // Handle detection process
    const handleDetect = async () => {
        if (!file) {
            alert('Please upload a file before detecting.');
            return;
        }
    
        setProcessing(true);
    
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await fetch('http://localhost:5000/detect', {
                method: 'POST',
                body: formData,
            });
    
            if (!response.ok) {
                const errorText = await response.text();  // Get raw error message or HTML
                console.error('Error response:', errorText);  // Log the error
                throw new Error(errorText);  // Throw an error with the response text
            }
    
            const responseText = await response.json();  // Parse the response as JSON
            console.log('Response:', responseText);  // Log the parsed response
    
            // Process the detected license plates or CSV link
            if (responseText.license_plates && responseText.license_plates.length > 0) {
                setLicensePlate(responseText.license_plates.map((item) => item.text).join(', '));
                setOutputFile(null);
            } else if (responseText.csv_download_link) {
                setOutputFile(responseText.csv_download_link);
                setLicensePlate(null);
            } else {
                alert('No license plates detected.');
            }
        } catch (error) {
            console.error('Error during detection:', error);
            alert(`An error occurred while processing the file: ${error.message}`);
        } finally {
            setProcessing(false);
        }
    };
    
   

    return (
        <div className="p-8 font-sans flex flex-col items-center bg-slate-600">
            {/* File Upload Container */}
            <div className="border-2 w-1/2 border-dashed border-gray-400 rounded-lg p-8 text-center mb-6 mt-4">
                <input
                    type="file"
                    accept="image/*,video/*"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="file-upload"
                    disabled={processing}  // Disable file input while processing
                />
                <label
                    htmlFor="file-upload"
                    className="cursor-pointer text-white hover:underline"
                >
                    Click here to upload a video
                </label>
                {file && <p className="mt-4 text-gray-600">File selected: {file.name}</p>}
            </div>

            {/* Detect Button */}
            <div className="text-center mb-6">
                <button
                    onClick={handleDetect}
                    className={`px-6 py-2 text-lg text-white rounded ${
                        processing ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
                    }`}
                    disabled={processing}
                >
                    {processing ? 'Processing...' : 'Detect'}
                </button>
            </div>

            {/* Display License Plate for Image */}
            {licensePlate && (
                <div className="border border-gray-300 rounded-lg p-6 text-center mt-6">
                    <h2 className="text-xl font-semibold text-gray-800">License Plate Detected</h2>
                    <p className="mt-4 text-gray-600">License Plate: {licensePlate}</p>
                </div>
            )}

            {/* Output Container for Video */}
            {outputFile && (
                <div className="border border-gray-300 rounded-lg p-6 text-center mt-6">
                    <h2 className="text-xl font-semibold text-gray-800">Detection Results</h2>
                    <a
                        href={outputFile}
                        download="results.csv"
                        className="text-blue-500 hover:underline mt-4 block"
                    >
                        Download CSV Output
                    </a>
                </div>
            )}
        </div>
    );
};

export default Upload;
