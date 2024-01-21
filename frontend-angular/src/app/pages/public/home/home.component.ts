import { Component } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { RouterModule } from '@angular/router';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  AuthService, AuthData,
          LojaService } from '../../../services/services';

import { LojaResponse } from '../../../models/models';
import { UserService } from '../../../services/user.service';
import { FormsModule } from '@angular/forms';

export class Loja {

  celular: string
  email: string
  endereco: any
  imagem_cadastro: string
  nome: string
  telefone: string
  username: string
  uuid: string
  seguindo: boolean | null

  constructor(response: any) {
    this.celular = response.celular
    this.email = response.email
    this.endereco = response.endereco
    this.imagem_cadastro = response.imagem_cadastro
    this.nome = response.nome
    this.telefone = response.telefone
    this.username = response.username
    this.uuid = response.uuid
    this.seguindo = null
  }
}


@Component({
  selector: 'app-user-home',
  standalone: true,
  imports: [RouterModule, SpinnerComponent, FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.sass'
})
export class UserHomeComponent {

  userData: BehaviorSubject<AuthData | null>
  lojas: BehaviorSubject<Array<Loja>>

  constructor (
    private authService: AuthService,
    private lojaService: LojaService,
    private userService: UserService
  ) {
    this.userData = authService.userData
    this.lojas = new BehaviorSubject<Array<Loja>>([])
  }

  ngOnInit() {
    this.lojaService.getAll().subscribe({
      next: (result: any) => {
        let payload = result.payload
        let lojas = payload.map((item: any) => new Loja(item))
        this.checkIfFollows(lojas)
        this.lojas.next(lojas);
      },
      error: (response) => {
        alert('Erro na requisição dos dados');
        console.log({response: response})
      }
    })
  }

  checkIfFollows(lojas: Array<Loja>) {
    lojas.forEach((loja: any) => {
      this.userService.checkIfFollows(loja).subscribe({
        next: (result: any) => {
          loja.seguindo = result.result
        },
        error: (result) => {
          console.error(result)
        }
      })
    });
  }

  followLoja(event: Event, loja: Loja) {

    let checkbox = event.target as HTMLInputElement
    let follow = checkbox.checked
    checkbox.disabled = true

    this.userService.followLoja(follow, loja).subscribe({
      next: (result: any) => {
        checkbox.disabled = false

        if (follow) {
          alert('Seguiu a loja com sucesso!')
        } else {
          alert('Deixou de seguir a loja com sucesso!')
        }

      },
      error: (result) => {
        console.error({result: result})
        checkbox.disabled = false
      }
    })
  }
}
