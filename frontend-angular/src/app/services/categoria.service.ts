import { AuthService, CompanyAuthData } from './auth.service';

import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';


import { CategoriaBodyRequest, CategoriaResponse } from '../models/models';

@Injectable({ providedIn: 'root' })
export class CategoriaService {

  baseUrl: string
  companyData: CompanyAuthData | null

  constructor(private http: HttpClient, private authService: AuthService) {
    this.baseUrl = `${environment.host}/categorias`
    this.companyData = authService.currentCompany()
  }

  getOne(uuid: string) {
    let obs = this.http.get(`${this.baseUrl}/${uuid}`)
    return obs
  }

  getAll(companyUUID: string):Observable<Object> {
    let params = new HttpParams()
      .set('loja_uuid', companyUUID)

    let observable = this.http.get(`${this.baseUrl}/`, {params: params})
    return observable
  }

  save(body: CategoriaBodyRequest) {
    let observable = this.http.post(
      this.baseUrl, body,
      { headers: { Authorization: `Bearer ${this.companyData?.access_token}` } }
    )
    return observable
  }

  delete(item: CategoriaResponse) {
    let observable = this.http.delete(
      `${this.baseUrl}/${item.uuid}`,
      { headers: { Authorization: `Bearer ${this.companyData?.access_token}` } }
    )
    return observable
  }
}

