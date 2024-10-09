const path = require('path');

module.exports = {
  entry: {
    popup: './popup.js',  // Your main popup file that uses jsQR
    background: './background.js'  // Your background script
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.js$/,  // Apply babel-loader to all JavaScript files
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],  // Use the preset to support modern JavaScript
          }
        }
      }
    ]
  }
};
