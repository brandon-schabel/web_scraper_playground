const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const profileSchema = new Schema({
  name: String,
  image_url: String,
  reason: String,
  liked: String,
  datetime: Date,
  age: Number,
  attributes: {
    smile: Number,
    gender: String,
    hair: [{
      color: String,
      confidence: Number
    }]
  }
})

// a model is a collection in the mongoDB based on the schema bookSchema, and we are exporting that
module.exports = mongoose.model("Profile", profileSchema, 'profile');
