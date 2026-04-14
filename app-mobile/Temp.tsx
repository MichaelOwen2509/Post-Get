import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';

export default function App() {
  const [nome, setNome] = useState('');
  const [senha, setSenha] = useState('');
  const [idLivro, setIdLivro] = useState('');

  const alugarLivro = async () => {
    try {
      const resposta = await fetch('http://10.67.237.92:8000/alugar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nome: nome,
          senha: senha,
          id_livro: parseInt(idLivro) 
        }),  
      });

      // Lemos o pacote que o Python devolveu
      const dados = await resposta.json();

      if (resposta.ok) {
        Alert.alert('Sucesso!', dados.Sucesso);
      } 
      else {
        Alert.alert('Ops, deu erro!', dados.detail.erro || dados.detail);
      }
      
    } catch (error) {
      Alert.alert('Erro de Conexão', 'Não foi possível achar o servidor FastAPI.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Biblioteca  hhApp</Text>

      <TextInput
        style={styles.input}
        placeholder="Digite seu nome"
        value={nome}
        onChangeText={setNome} 
      />

      <TextInput
        style={styles.input}
        placeholder="Digite sua senha"
        value={senha}
        onChangeText={setSenha}
        secureTextEntry={true} 
      />

      <TextInput
        style={styles.input}
        placeholder="ID do Livro (Ex: 1 ou 2)"
        value={idLivro}
        onChangeText={setIdLivro}
        keyboardType="numeric" 
      />

      <Button title="Confirmar Aluguel" onPress={alugarLivro} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  titulo: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 30,
  },
  input: {
    height: 50,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    marginBottom: 15,
    paddingHorizontal: 10,
    fontSize: 16,
  },
});