// signature.go
package main

import (
	"fmt"

	"github.com/cloudflare/circl/sign/mldsa/mldsa87"
)

// SignatureScheme wraps Dilithium keypair
type SignatureScheme struct {
	Pub  *mldsa87.PublicKey
	Priv *mldsa87.PrivateKey
	Ctx  []byte
}

// NewSignatureScheme generates a new Dilithium keypair with optional context
func NewSignatureScheme(ctx []byte) (*SignatureScheme, error) {
	pub, priv, err := mldsa87.GenerateKey(nil)
	if err != nil {
		return nil, fmt.Errorf("key generation failed: %w", err)
	}
	return &SignatureScheme{
		Pub:  pub,
		Priv: priv,
		Ctx:  ctx,
	}, nil
}

func (s *SignatureScheme) Sign(msg []byte) ([]byte, error) {
	sig := make([]byte, mldsa87.SignatureSize)
	// SignTo fills `sig`
	if err := mldsa87.SignTo(s.Priv, msg, nil, true, sig); err != nil {
		return nil, err
	}
	return sig, nil
}

// Verify checks a Dilithium signature over msg
func (s *SignatureScheme) Verify(msg []byte, sig []byte) bool {

	return mldsa87.Verify(s.Pub, msg, s.Ctx, sig)
}
