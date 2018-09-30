import React, { Component } from 'react';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';

// components
import ListProfiles from './components/ListProfiles'

//setting up our graphql endpoint
const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql'
})

class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
      <div id="main">
        <h1>Profile Data</h1>
        <ListProfiles></ListProfiles>
      </div>
      </ApolloProvider>
    );
  }
}

export default App;
