import { Endereco } from "./endereco";

export class User {

  ativo: boolean;
  celular: string;
  email: string;
  modo_de_cadastro: string;
  nome: string;
  passou_pelo_primeiro_acesso: boolean;
  telefone: string;
  username: string;
  endereco: Endereco
  uuid: string;

  constructor(result: any) {
    this.ativo = result.ativo;
    this.celular = result.celular;
    this.email = result.email;
    this.modo_de_cadastro = result.modo_de_cadastro;
    this.nome = result.nome;
    this.endereco = result.endereco
    this.passou_pelo_primeiro_acesso = result.passou_pelo_primeiro_acesso;
    this.telefone = result.telefone;
    this.username = result.username;
    this.uuid = result.uuid;
  }
}

