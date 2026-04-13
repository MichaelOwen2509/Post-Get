import { useState } from "react"
import { Alert, Button, StyleSheet, Text, TextInput, View } from "react-native";

export default function App(){
  const [nome,setNome] = useState('');
  const [senha, setSenha] = useState('');
  const [idLivro, setIdLivro] = useState('');

  const alugarLivro = async() => {
    try{
      const resposta = await fetch("http://10.73.109.92:8000/alugar",{
        method: 'POST',
        headers: { 'Content-Type' : 'application/json'},
        body: JSON.stringify({
          nome: nome,
          senha: senha,
          id_livro: parseInt(idLivro),
        }),
      });

      const dados = await resposta.json();

      if (dados.ok){
        Alert.alert('Sucesso!', dados.Sucesso)
      }else{
        Alert.alert('Erro!', dados.Erro)
      }

    }catch (erro) {
      Alert.alert("Erro de conexão", "API não encontrada!")
    }
  }
  
  return(
        <View style={styles.container}>
      <Text style={styles.titulo}>BibliotecaApp</Text>

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