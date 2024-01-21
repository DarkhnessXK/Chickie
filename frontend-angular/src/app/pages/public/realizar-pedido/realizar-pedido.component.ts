import { Component } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { v4 as uuidv4 } from 'uuid';
import { NgxMaskDirective } from 'ngx-mask';
import { CommonModule } from '@angular/common';
import { ButtonHandler } from '../../../handlers/button';

import {  ProdutoResponse, CategoriaResponse, LojaResponse,
          ItemPedido, Endereco, User } from '../../../models/models';

import {  PedidoService, CategoriaService,
          AuthService, LojaService, AuthData,
          ProdutoService } from '../../../services/services';


@Component({
  selector: 'app-loja',
  standalone: true,
  imports: [
    FormsModule,
    NgxMaskDirective,
    RouterModule,
    CommonModule
  ],
  templateUrl: './realizar-pedido.component.html',
  styleUrl: './realizar-pedido.component.sass'
})
export class RealizarPedidoComponent {

  loja: LojaResponse | null
  companyProducts: BehaviorSubject<Array<ProdutoResponse>>
  companyData: AuthData | null
  companyCategorias: BehaviorSubject<Array<CategoriaResponse>>
  produtoValue: any
  numeroDeItens: BehaviorSubject<Array<ItemPedido>>
  userData: AuthData | null
  endereco: Endereco
  celular: string
  observacoes: string
  comentarios: string
  lojaUUID: string

  constructor(

    private route: ActivatedRoute,
    private produtoService: ProdutoService,
    private categoriaService: CategoriaService,
    private lojaService: LojaService,
    private authService: AuthService,
    private pedidoService: PedidoService

  ) {
    this.userData = null
    this.lojaUUID = ''
    this.observacoes = ''
    this.comentarios = ''
    this.loja = null
    this.companyData = null
    this.produtoValue = null
    this.companyProducts = new BehaviorSubject<Array<ProdutoResponse>>([]);
    this.companyCategorias = new BehaviorSubject<Array<CategoriaResponse>>([]);
    this.numeroDeItens = new BehaviorSubject<Array<ItemPedido>>([]);
    this.celular = ''
    this.endereco = {
      uf: '',
      cidade: '',
      logradouro: '',
      numero: '',
      bairro: '',
      cep: '',
      complemento: '',
    }
  }

  ngOnInit(): void {
    this.userData = this.authService.currentUser()
    this.celular = this.userData?.celular || ''
    if (this.userData?.endereco) {
      this.endereco = this.userData.endereco
    }
    this.route.params.subscribe(params => {
      this.lojaUUID = params['lojaID'];
      this.fetchLoja(this.lojaUUID);

      this.numeroDeItens = new BehaviorSubject<Array<ItemPedido>>([{
        quantidade: 1,
        produto_uuid: '',
        uuid: uuidv4(),
        observacoes: '',
        loja_uuid: this.lojaUUID
      }]);

      this.fetchProducts(this.lojaUUID)
    })
  }



  addItem() {
    const randomUUID: string = uuidv4();
    this.numeroDeItens.value.push({
      quantidade: 1,
      produto_uuid: '',
      uuid: randomUUID,
      observacoes: '',
      loja_uuid: this.lojaUUID
    })
  }

  removeItem(item: any) {

    if (!(this.numeroDeItens.value.length > 1)) {
      throw new Error('O pedido necessita de ao menos um pedido!')
    }

    let newArr = this.numeroDeItens.getValue()
    newArr = newArr.filter(u => item.uuid != u.uuid)
    this.numeroDeItens.next(newArr)
  }

  private fetchLoja(companyUUID: string): void {
    this.lojaService.getOne(companyUUID).subscribe({
      next: (response: any) => {
        this.loja = {...response};
      },
      error: (response: HttpErrorResponse) => {
        let msg = '132: Erro na requisição dos dados da loja!';
        alert(msg); throw new Error(msg);
      }
    })
  }

  fetchProducts(companyUUID: string) {
    this.produtoService.getAll(companyUUID).subscribe({
      next: (result: any) => {
        let payload = result.payload
        if (Array.isArray(payload)) {
          this.companyProducts.next(payload)
          this.fetchCategoriasForProducts()
        }
      },
      error: (response: HttpErrorResponse) => {
        let msg = '148: Erro ao buscar pelos produtos'
        alert(msg); throw new Error(msg)
      }
    })
  }

  fetchCategoriasForProducts() {
    for (let produto of this.companyProducts.value) {

      this.categoriaService.getOne(produto.categoria_uuid).subscribe({
        next: (response) => {
          produto.categoria = response
        },
        error: (response: HttpErrorResponse) => {
          let msg = '162: Erro ao buscar pelas categorias'
          alert(msg); throw new Error(msg)
        }
      })

    }
  }

  getPrecoTotal():number {
    let total = 0
    for (let item of this.numeroDeItens.value) {
      let parcial = (
        item.quantidade * this.getProdutoPreco(item.produto_uuid)
      )
      total += parcial
    }

    return total
  }

  getProdutoPreco(produtoUUID: string): number {
    for (let produto of this.companyProducts.value) {
      if (produto.uuid == produtoUUID) {
        let found = produto.preco_hoje || produto.preco
        return found
      }
    }
    return 0
  }

  getProdutoPrecoBase(produtoUUID: string): number {
    for (let produto of this.companyProducts.value) {
      if (produto.uuid == produtoUUID) {
        let found = produto.preco
        return found
      }
    }
    return 0
  }

  cadastrarPedido(event: Event) {

    let user_uuid = null;
    let button = new ButtonHandler(event)
    button.disable('Enviando o pedido...')
    if (this.userData && this.userData.uuid) {
      user_uuid = this.userData.uuid
    }

    let numeroCelular = this.celular.replace(/\D/g, '');
    if (numeroCelular.length != 11) {
      alert('O numero de celular precisa ter 11 digitos contando com o DDD!')
      return
    }

    if (!this.loja) {
      alert('Loja não encotrada!')
      return
    }

    let itens = this.numeroDeItens.getValue()
    for (let item of itens) {
      if (!item.produto_uuid) {
        alert('O campo produto é obrigatório!')
        return
      }
    }

    let body = {
      celular: numeroCelular,
      data_hora: new Date().toISOString(),
      endereco: this.endereco,
      frete: this.loja.frete || 0,
      itens: itens.map(item => ({
        produto_uuid: item.produto_uuid,
        quantidade: item.quantidade,
        observacoes: item.observacoes
      })),
      loja_uuid: this.loja.uuid,
      comentarios: this.comentarios,
      status_uuid: null,
      usuario_uuid: user_uuid,
    }

    if (this.userData) {
      body.usuario_uuid = this.userData.uuid
    }

    this.pedidoService.save(body).subscribe({
      next: (response) => {
        button.enable()
        console.log({response: response})
        alert('Pedido Cadastrado com sucesso!')
        this.clearInputs()
      },
      error: (response) => {
        button.enable()
        console.log({response: response})
        alert('Erro no cadastro dos produtos')
      }
    })
  }

  clearInputs() {
    this.comentarios = ''
    this.companyProducts = new BehaviorSubject<Array<ProdutoResponse>>([]);
    this.companyCategorias = new BehaviorSubject<Array<CategoriaResponse>>([]);
    this.numeroDeItens = new BehaviorSubject<Array<ItemPedido>>([]);
    this.ngOnInit()
  }
}
