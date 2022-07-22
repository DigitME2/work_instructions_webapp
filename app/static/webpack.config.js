const precss = require('precss');
const autoprefixer = require('autoprefixer');

module.exports = {
    entry: './app.js',
    output: {
        filename: 'bundle.js',
    },
    module: {
        rules: [{
            test: /\.scss$/,
            use: [
                { loader: 'style-loader' },
                { loader: 'css-loader' },
                {
                    loader: 'postcss-loader',
                    options: {
                    },
                },
                { loader: 'sass-loader' },
            ],
        }],
    },
};