import React, { useState } from 'react';
import Layout from '../components/Layout';
import api from '../services/api';
import { toast } from 'react-toastify';

const Interview = () => {
    const [formData, setFormData] = useState({
        jobTitle: '',
        company: '',
        jobDescription: ''
    });
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [answers, setAnswers] = useState({});
    const [feedback, setFeedback] = useState({});
    const [feedbackLoading, setFeedbackLoading] = useState({});

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleGenerate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await api.generateQuestions(
                formData.jobTitle,
                formData.company,
                formData.jobDescription
            );
            // Assuming response is { questions: ["q1", "q2", ...] } or similar
            // Adjust based on actual API response structure
            setQuestions(response.questions || response);
            toast.success('Interview questions generated!');
        } catch (error) {
            console.error('Error generating questions:', error);
            toast.error('Failed to generate questions');
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerChange = (index, value) => {
        setAnswers({ ...answers, [index]: value });
    };

    const handleGetFeedback = async (index, question) => {
        const answer = answers[index];
        if (!answer) {
            toast.warning('Please write an answer first');
            return;
        }

        setFeedbackLoading({ ...feedbackLoading, [index]: true });
        try {
            const response = await api.getFeedback(formData.jobTitle, question, answer);
            setFeedback({ ...feedback, [index]: response.feedback || response });
        } catch (error) {
            console.error('Error getting feedback:', error);
            toast.error('Failed to get feedback');
        } finally {
            setFeedbackLoading({ ...feedbackLoading, [index]: false });
        }
    };

    return (
        <Layout>
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">AI Interview Preparation</h1>

                {/* Input Form */}
                <div className="bg-white shadow rounded-lg p-6 mb-8">
                    <h2 className="text-xl font-semibold mb-4">Job Details</h2>
                    <form onSubmit={handleGenerate} className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Job Title</label>
                                <input
                                    type="text"
                                    name="jobTitle"
                                    value={formData.jobTitle}
                                    onChange={handleChange}
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Company</label>
                                <input
                                    type="text"
                                    name="company"
                                    value={formData.company}
                                    onChange={handleChange}
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Job Description</label>
                            <textarea
                                name="jobDescription"
                                value={formData.jobDescription}
                                onChange={handleChange}
                                rows={4}
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Paste the job description here..."
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
                        >
                            {loading ? 'Generating Questions...' : 'Generate Interview Questions'}
                        </button>
                    </form>
                </div>

                {/* Questions List */}
                {questions.length > 0 && (
                    <div className="space-y-6">
                        <h2 className="text-2xl font-bold text-gray-900">Practice Questions</h2>
                        {questions.map((q, index) => (
                            <div key={index} className="bg-white shadow rounded-lg p-6">
                                <h3 className="text-lg font-medium text-gray-900 mb-3">
                                    {index + 1}. {q}
                                </h3>
                                <div className="space-y-3">
                                    <textarea
                                        value={answers[index] || ''}
                                        onChange={(e) => handleAnswerChange(index, e.target.value)}
                                        rows={3}
                                        className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="Type your answer here..."
                                    />
                                    <button
                                        onClick={() => handleGetFeedback(index, q)}
                                        disabled={feedbackLoading[index]}
                                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                    >
                                        {feedbackLoading[index] ? 'Analyzing...' : 'Get AI Feedback'}
                                    </button>
                                </div>

                                {feedback[index] && (
                                    <div className="mt-4 p-4 bg-green-50 rounded-md border border-green-200">
                                        <h4 className="text-sm font-bold text-green-800 mb-1">Feedback:</h4>
                                        <p className="text-sm text-green-700 whitespace-pre-wrap">{feedback[index]}</p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </Layout>
    );
};

export default Interview;
