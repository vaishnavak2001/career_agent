import React, { useState } from 'react';
import Layout from '../components/Layout';
import api from '../services/api';

const ResumeUpload = () => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setMessage('');

        try {
            await api.uploadResume(file);
            setMessage('Resume uploaded successfully!');
            setFile(null);
        } catch (error) {
            setMessage('Failed to upload resume.');
            console.error(error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                            Upload your Resume
                        </h3>
                        <div className="mt-2 max-w-xl text-sm text-gray-500">
                            <p>
                                Upload your base resume (PDF or DOCX). The agent will use this to tailor applications for specific jobs.
                            </p>
                        </div>
                        <div className="mt-5 sm:flex sm:items-center">
                            <div className="w-full sm:max-w-xs">
                                <input
                                    type="file"
                                    onChange={handleFileChange}
                                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                                />
                            </div>
                            <button
                                type="button"
                                onClick={handleUpload}
                                disabled={!file || uploading}
                                className={`mt-3 w-full inline-flex items-center justify-center px-4 py-2 border border-transparent shadow-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm ${(!file || uploading) ? 'opacity-50 cursor-not-allowed' : ''}`}
                            >
                                {uploading ? 'Uploading...' : 'Save'}
                            </button>
                        </div>
                        {message && (
                            <div className={`mt-4 text-sm ${message.includes('success') ? 'text-green-600' : 'text-red-600'}`}>
                                {message}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ResumeUpload;
