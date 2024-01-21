import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FileDataRequest } from '../models/models';
import { environment } from '../../environments/environment';
import { UserSignUpRequest } from './signup.service';
import { CompanyAuthData } from './auth.service';



@Injectable({ providedIn: 'root' })
export class LojaService {

  baseUrl: string

  constructor(private http: HttpClient) {
    this.baseUrl = `${environment.host}/loja`
  }

  getOne(uuid: string): Observable<Object> {
    let observable = this.http.get(this.baseUrl.concat(`/${uuid}`))
    return observable
  }

  getAll():Observable<Object> {
    let observable = this.http.get(`${this.baseUrl}/`)
    return observable
  }

  getAllProducts(
    companyUUID: string,
    categoryUUID?: string
  ):Observable<Object> {
    let url = this.baseUrl.concat(`/${companyUUID}/produtos`)
    if (categoryUUID) {
      url = url.concat(`?categoria_uuid=${categoryUUID}`)
    }
    let observable = this.http.get(url)
    return observable
  }

  atualizarImagemCadastro(body: FileDataRequest, companyData: any) {
    let observable = this.http.post(
      this.baseUrl.concat(`/imagem_cadastro`), body, {
        headers: { Authorization: `Bearer ${companyData?.access_token}`
      }
    })

    return observable
  }

  getAllCostumers(companyData: any) {
    let observable = this.http.get(
      this.baseUrl.concat(`/clientes/`), {
        headers: { Authorization: `Bearer ${companyData?.access_token}`
      }
    })

    return observable
  }

  atualizarCadastro(body: any, companyData: any) {

    if (!companyData) {
      let msg = 'Dados da empresa não encontrados!'
      alert(msg); throw new Error(msg)
    }

    console.log({H: { Authorization: `Bearer ${companyData?.access_token}` }})
    let observable = this.http.put(
      this.baseUrl.concat(`/${companyData.loja.uuid }`), body, {
        headers: { Authorization: `Bearer ${companyData?.access_token}` }
    })

    return observable
  }

  cadastrarUser(
    companyUUID: string,
    body: UserSignUpRequest,
    authData: CompanyAuthData
  ) {
    let path = `/cliente_v2/${companyUUID}`
    let obs = this.http.post(this.baseUrl.concat(path), body, { headers: {
      Authorization: `Bearer ${authData.access_token}`
    } })
    return obs
  }
}
