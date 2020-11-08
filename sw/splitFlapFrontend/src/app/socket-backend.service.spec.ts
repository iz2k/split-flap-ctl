import { TestBed } from '@angular/core/testing';

import { SocketBackendService } from './socket-backend.service';

describe('SocketBackendService', () => {
  let service: SocketBackendService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocketBackendService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
