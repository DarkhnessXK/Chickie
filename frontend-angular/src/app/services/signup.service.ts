import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';


export type EmpresaSignUpRequest = {

  nome: string,
  username: string,
  email: string,
  telefone: string,
  celular: string,
  password: string
  image_bytes: string | ArrayBuffer
  image_filename: string

}

export type UserSignUpRequest = {

  celular: string,
  email: string,
  nome: string,
  password: string,
  telefone: string,
  username: string

  bairro: string,
  cep: string,
  cidade: string,
  complemento: string,
  logradouro: string,
  numero: string,
  uf: string,

  modo_de_cadastro: string

}


@Injectable({ providedIn: 'root' })
export class SignupService {

  private companySignupUrl: string
  private userSignupUrl: string

  constructor(private http: HttpClient) {
    this.companySignupUrl = `${environment.host}/loja/signup`
    this.userSignupUrl = `${environment.host}/user/signup`
  }

  doCompanySignUp(body: EmpresaSignUpRequest) {
    let obs = this.http.post(this.companySignupUrl, body)
    return obs
  }

  doUserSignUp(body: UserSignUpRequest) {
    let obs = this.http.post(this.userSignupUrl, body)
    return obs
  }

}
