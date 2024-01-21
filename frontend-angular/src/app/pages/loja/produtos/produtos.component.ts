import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  ProdutoResponse, CategoriaResponse,
          Response201ImageCreatedWrapper} from '../../../models/models';

import {  CompanyAuthData, AuthService,
          ProdutoService, CategoriaService } from '../../../services/services';


@Component({
  selector: 'app-cadastro-produto',
  standalone: true,
  imports: [FormsModule, RouterModule, SpinnerComponent],
  templateUrl: './produtos.component.html',
  styleUrl: './produtos.component.sass'
})
export class ProdutosComponent {

  nomeValue: string
  descricaoValue: string
  precoValue: number | null
  categoriaValue: any
  loading: boolean

  companyProducts: BehaviorSubject<Array<ProdutoResponse>>
  companyCategorias: BehaviorSubject<Array<CategoriaResponse>>
  companyData: CompanyAuthData | null
  companyUUID: string | null

  constructor(
    private produtoService: ProdutoService,
    private authService: AuthService,
    private categoriaService: CategoriaService,
  ) {
    this.loading = false
    this.companyCategorias = new BehaviorSubject<Array<CategoriaResponse>>([])
    this.companyProducts = new BehaviorSubject<Array<ProdutoResponse>>([])
    this.companyData = this.authService.currentCompany()
    this.companyUUID = null

    this.nomeValue = ''
    this.descricaoValue = ''
    this.precoValue = null
    this.categoriaValue = ''
  }

  fetchProducts() {
    this.loading = true
    if (!this.companyData) {
      let msg =' Dados da empresa não encontrados!'
      alert(msg); throw new Error(msg)
    }

    this.produtoService.getAll(this.companyData.loja.uuid).subscribe({
      next: (response: any) => {
        let payload = response.payload
        this.companyProducts.next(payload)
        this.fetchCategoriasForProducts()
      },
      error: (response) => {
        let msg = 'Erro ao buscar pelos produtos'
        alert(msg); console.log(response); throw new Error(msg)
      }
    })
  }

  fetchCategoriasForProducts() {
    for (let produto of this.companyProducts.value) {

      if (!this.companyData) {
        let msg =' Dados da empresa não encontrados!'
        alert(msg); throw new Error(msg)
      }

      this.categoriaService.getOne(produto.categoria_uuid).subscribe({
        next: (response) => {
          produto.categoria = response
        },
        error: (response) => {
          let msg = 'Erro ao buscar pelas categorias'
          alert(msg); console.log(response); throw new Error(msg)
        }
      })
    }
    this.loading = false
  }

  fetchCategorias() {
    if (!this.companyData) {
      alert('Dados da empresa não encontrados!')
      throw new Error('Dados da empresa não encontrados!')
    }
    this.categoriaService.getAll(this.companyData.loja.uuid).subscribe({
      next: (response: any) => {
        this.companyCategorias.next(response)
      },
      error: (response) => {
        let msg = '101: Dados de categorias não encontrados!'
        alert(msg); console.log(msg); throw new Error(msg)
      },
    })
  }

  ngOnInit() {
    this.fetchCategorias()
    this.fetchProducts()
  }

  cadastrarProduto() {

    if (!this.companyData) {
      alert('Nenhuma empresa logada!')
      return
    }

    let inputs: Array<{ [key: string]: string | number | null }> = [
      {Nome: this.nomeValue},
      {Descricao: this.descricaoValue},
      {Preco: this.precoValue},
      {Categoria: this.categoriaValue}
    ]

    for (let inputData of inputs) {
      let title = Object.keys(inputData)[0];
      let element = inputData[title];

      if (element == null || element == undefined || element == '') {
        let msg = `O input ${title} é requerido!`;
        alert(msg); throw new Error(msg)
      }
    }

    let body = {
      loja_uuid: this.companyData.loja.uuid,
      categoria_uuid: this.categoriaValue,
      nome: this.nomeValue,
      descricao: this.descricaoValue,
      preco: Number(this.precoValue || 0),
      image_bytes: ''
    }

    this.produtoService.save(body).subscribe({
      next: (response) => {
        let r = new Response201ImageCreatedWrapper(response)
        alert('Item adicionado com sucesso!')
        this.categoriaService.getOne(this.categoriaValue).subscribe({
          next: (response) => {
            let newProduct = {
              ...body,
              uuid: r.uuid,
              categoria: response,
              image_url: r.image_url
            }
            this.companyProducts.value.push(newProduct)
          }
        })
      },
      error: (response) => {
        let msg = 'Erro no cadastro do item';
        alert(msg); throw new Error(msg)
      }
    })

  }

}
