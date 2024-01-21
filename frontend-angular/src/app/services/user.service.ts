import { Injectable } from '@angular/core';
import { LojaResponse } from '../models/loja';
import { AuthData, AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  urlBase: string
  userData: AuthData | null

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
    this.userData = this.authService.currentUser()
    this.urlBase = `${environment.host}/user`
  }

  followLoja(follow: boolean, loja: any) {

    if (!this.userData) {
      let msg = 'Dados de user não encontrados'
      alert(msg); throw new Error(msg)
    }

    let headers = { Authorization: `Bearer ${this.userData.access_token}` }

    let path = '/seguir-loja'
    let body = {
      loja_uuid: loja.uuid,
      usuario_uuid: this.userData.uuid,
      follow: follow
    }
    return this.http.post(this.urlBase.concat(path), body, {
      headers: headers
    })
  }

  checkIfFollows(loja: any) {
    if (!this.userData) {
      let msg = 'Dados de user não encontrados'
      alert(msg); throw new Error(msg)
    }

    let headers = { Authorization: `Bearer ${this.userData.access_token}` }
    let path = `/segue-loja/${loja.uuid}`

    return this.http.get(this.urlBase.concat(path), {
      headers: headers
    })
  }
}
