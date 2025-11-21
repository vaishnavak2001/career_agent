/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#2557a7', // Indeed blue-ish
                secondary: '#f3f2f1', // Light gray background
            }
        },
    },
    plugins: [],
}
