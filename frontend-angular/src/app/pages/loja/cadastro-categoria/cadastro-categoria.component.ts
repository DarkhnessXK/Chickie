import { Component } from '@angular/core';
import { CategoriaResponse, Response201Wrapper } from '../../../models/models';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { ButtonHandler } from '../../../handlers/button';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  CompanyAuthData, AuthService,
          CategoriaService } from '../../../services/services';


@Component({
  selector: 'app-cadastro-categoria',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, SpinnerComponent],
  templateUrl: './cadastro-categoria.component.html',
  styleUrl: './cadastro-categoria.component.sass'
})
export class CadastroCategoriaComponent {

  companyData: CompanyAuthData | null
  categorias: BehaviorSubject<Array<CategoriaResponse>>
  descricaoValue: string
  nomeValue: string
  loading: boolean

  constructor (private service: CategoriaService, authService: AuthService) {
    this.loading = false
    this.descricaoValue = ''
    this.nomeValue = ''
    this.companyData = authService.currentCompany()
    this.categorias = new BehaviorSubject<Array<CategoriaResponse>>([])
  }

  ngOnInit() {
    this.loading = true
    if (this.companyData) {
      this.service.getAll(this.companyData.loja.uuid).subscribe({
        next: (result: any) => {
          this.loading = false
          let payload = result.payload
          if (Array.isArray(payload)) {
            this.categorias.next(payload)
          }
        },
        error: (result: Object) => {
          throw new Error(JSON.stringify(result))
        }
      })
    }
  }

  registerCategoria(event: Event) {
    let button = new ButtonHandler(undefined, 'btn_cad')
    button.disable('Cadastrando...')
    if (!this.companyData) {
      alert('Nenhuma empresa logada!')
      throw new Error('Nenhuma empresa logada!')
    }

    let body = {
      descricao: this.descricaoValue,
      loja_uuid: this.companyData.loja.uuid,
      nome: this.nomeValue
    }

    this.service.save(body).subscribe({
      next: (response) => {
        button.enable()
        let r = new Response201Wrapper(response)
        alert('Item salvo com sucesso!');
        this.categorias.value.push({...body, uuid: r.uuid})
      },
      error: (response) => {
        button.enable()
        alert('Erro no registro da categoria');
        throw new Error(JSON.stringify(response))
      }
    })
  }


  deleteCategoria(event: Event, categoria: CategoriaResponse) {

    let button = new ButtonHandler(event)
    button.disable('Removendo...')

    this.service.delete(categoria).subscribe({
      next: (response: Object) => {
        button.enable()
        let newArray = this.categorias.getValue()
        .filter(i => i.uuid != categoria.uuid)

        this.categorias.next(newArray)
        alert('Item removido');
      },
      error: (response: Object) => {
        button.enable()
        alert(
          `Erro na remoção da categoria. Verifique se ela possui produtos cadastrados`
        );
        throw new Error(JSON.stringify(response))
      }
    })
  }


}
