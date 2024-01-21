import { Endereco } from "./endereco";


export type Pedido = {
  celular: string;
  data_hora: string;
  endereco_uuid: string | null;
  endereco: Endereco;
  status: any;
  frete: number;
  itens: Array<{
    loja_uuid: string,
    pedido_uuid: string,
    produto_uuid: string,
    produto_nome: string,
    produto_descricao: string,
    subtotal: number,
    quantidade: number,
    valor: number,
    observacoes: string,
    uuid: string,
  }>;
  loja_uuid: string;
  status_uuid: string | null;
  total: number
  uuid: string;
  concluido: boolean
  comentarios: string
};

